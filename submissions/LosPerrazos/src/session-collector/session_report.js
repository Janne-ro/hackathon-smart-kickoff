/**
 * Session Report — snapshots all session data (transcript, biomarkers)
 * into a JSON report before cleanup destroys the in-memory stores.
 *
 * Reports are saved to disk (./session-reports/) and cached in memory.
 */

const fs = require('fs');
const path = require('path');

const { getMessagesByChannel } = require('./conversation_store');
const thymiaStore = require('./integrations/thymia/thymia_store');

const logger = {
  info: (msg) => console.log(`INFO: ${msg}`),
  error: (msg) => console.error(`ERROR: ${msg}`),
};

const REPORTS_DIR = path.join(__dirname, 'session-reports');
const MAX_MEMORY_REPORTS = 50;

const reports = new Map();
const recentChannels = new Map();

if (!fs.existsSync(REPORTS_DIR)) {
  fs.mkdirSync(REPORTS_DIR, { recursive: true });
}

function generateReport(appId, channel, agentId, endReason = 'unknown') {
  // Idempotency: skip if we generated a report for this channel within 5s
  const recent = recentChannels.get(channel);
  if (recent && Date.now() - recent < 5000) {
    logger.info(`[SessionReport] Already generated for ${channel} ${Date.now() - recent}ms ago, skipping`);
    return getLatestReportByChannel(channel);
  }
  recentChannels.set(channel, Date.now());

  const reportId = `report_${channel}_${Date.now()}`;
  const now = new Date();

  // Snapshot transcript
  const transcript = getMessagesByChannel(appId, channel);

  // Snapshot Thymia biomarkers
  let thymiaMetrics = null;
  try {
    thymiaMetrics = thymiaStore.getMetrics(appId, channel);
  } catch (e) {
    logger.error(`[SessionReport] Failed to get Thymia metrics: ${e.message}`);
  }

  // Calculate session duration from transcript timestamps
  const timestamps = transcript.filter((m) => m.timestamp).map((m) => m.timestamp);
  const startedAt = timestamps.length > 0 ? new Date(Math.min(...timestamps)).toISOString() : null;
  const endedAt = now.toISOString();
  const durationSeconds =
    timestamps.length > 0 ? Math.round((now.getTime() - Math.min(...timestamps)) / 1000) : 0;

  const report = {
    id: reportId,
    version: '1.0',
    session: {
      channel,
      appId,
      agentId: agentId || null,
      startedAt,
      endedAt,
      durationSeconds,
      endReason,
    },
    transcript: transcript.map((m) => ({
      role: m.role,
      content: m.content || null,
      timestamp: m.timestamp || null,
      ...(m.tool_calls ? { tool_calls: m.tool_calls } : {}),
      ...(m.tool_call_id ? { tool_call_id: m.tool_call_id, name: m.name } : {}),
    })),
    biomarkers: {
      thymia: thymiaMetrics || null,
    },
    metadata: {
      generatedAt: now.toISOString(),
    },
  };

  // Cache in memory
  reports.set(reportId, report);
  if (reports.size > MAX_MEMORY_REPORTS) {
    const oldest = reports.keys().next().value;
    reports.delete(oldest);
  }

  // Save to disk
  const filePath = path.join(REPORTS_DIR, `${reportId}.json`);
  fs.writeFile(filePath, JSON.stringify(report, null, 2), (err) => {
    if (err) logger.error(`[SessionReport] Failed to write: ${err.message}`);
    else logger.info(`[SessionReport] Saved: ${filePath}`);
  });

  logger.info(
    `[SessionReport] Generated: ${reportId} (${transcript.length} messages, thymia=${!!thymiaMetrics}, duration=${durationSeconds}s)`
  );

  return report;
}

function getReport(reportId) {
  return reports.get(reportId) || null;
}

function getLatestReportByChannel(channel) {
  for (const [, report] of [...reports.entries()].reverse()) {
    if (report.session.channel === channel) return report;
  }
  return null;
}

function listReports() {
  return [...reports.values()].map((r) => ({
    id: r.id,
    channel: r.session.channel,
    endedAt: r.session.endedAt,
    durationSeconds: r.session.durationSeconds,
    transcriptLength: r.transcript.length,
    hasThymia: !!r.biomarkers.thymia,
  }));
}

module.exports = { generateReport, getReport, getLatestReportByChannel, listReports };
