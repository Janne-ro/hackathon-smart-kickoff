# How we build

This file aims to show how we worked with AI, not just what we built.

## Planning 
> "How did you use AI to plan your architecture, break down tasks, or explore approaches?"

Initially, we conducted a team brainstorming session, exploring ideas across multiple directions. Through collaborative discussion and iterative refinement, we gradually narrowed these down to a single concept that we all agreed upon. We did not use AI during this ideation phase.

Subsequently, we designed the system architecture by icmd-k vdentifying its main components (*C1 – AI Onboarding Chat* and *C2 – Dashboards*). We began with a high-level definition of each component and then progressively refined them into more concrete requirements. At this stage, we used ChatGPT 5.4 to validate our detailed architecture and ensure it aligned with the goals outlined in the initial [Motivation](README.md#Motivation) and [How It Works](README.md#how-it-works) sections of our README.

Finally, we organized the work into structured work packages, which were then distributed among the team members.

---

## Model choices 
> "Which AI models/tools did you use for development and why?"

**For coding:**
* *ChatGPT-5.3-Codex in Codex environment*: ChatGPT 5.3 Codex helped us quickly generate, debug, and optimize code with contextual understanding of programming logic.
* *Claude Opus*: We used Claude Opus for its advanced reasoning and code synthesis capabilities, which accelerated development of complex features.

**For research purposes:**
* *Gemini*: Gemini allowed us to ground our project in reliable academic and industry knowledge, ensuring our solutions were evidence-based and up-to-date.

---

## Prompting strategies 
> "What prompting techniques worked well? What didn't? Share example prompts that led to breakthroughs."

### Prompting techniques that worked well

* **Few-Shot Prompting**: Providing a few illustrative examples within the prompt helped the AI understand the desired format, style, and reasoning steps, reducing misinterpretations.
* **Prompt Iteration**: Repeatedly refining prompts based on AI output proved highly effective. Also asking the model to critique or improve its own response often led to more precise and actionable results.
* **Role or Persona Framing**: Assigning the AI a specific role (e.g., “You are a coding expert”) improved the relevance of the output and kept the responses focused on the task.

*Example prompt: "Lets build a second dashboard for the student. Lets plan the AI assesment first.  Preply already ask the following questions:  What do you want to learn? English (Language options)  [...] The idea is that the AI assistant also retrieves at least this information, in a conversational way of course. Other information migh also be asked. The things that are direct filters or options that the user selects, should be displayed in this dashboard so the user can change them in case that they were incorrect. We should not show the retention score, instead, we should show the user a motivation assesment of their proficiency, showing things that he does well and also areas of inprovement. [...] What do you think. Am i missing something? output a list of features for the student dashboard before start coding"*

### Prompting techniques that didn't work well

* **Zero-Shot Prompting**: Asking the model to generate output without context or examples often produced incomplete or inconsistent results, requiring many iterations to correct.
* **Single-Instruction Prompts for Complex Tasks**: Giving multi-step tasks in one instruction without breaking them down often led to misaligned outputs.

*Example prompt: " That already looks good but move the Find a professor button such that it is directly underneath the language skills section. Also change the colorscheme to pink/red (do research on the colorscheme of Preply to match). Finally, add something to help students understand their areas of improvement more."*

--- 

## Testing & iteration 
> "How did you verify AI-generated code? Did you use test-driven development, manual testing, or AI-assisted debugging?"

We used a **combination of manual testing and AI-assisted debugging**, which allowed us to quickly identify edge cases and validate behavior against expected outcomes. One example where this really helped was in evaluating the expected calculation for the dashboards at the interface between the AI onboarding chat and the dashboards for which we used manual tests. Additionally, it assisted with iteratively refining both our conversational flows and retention prediction models for an optimized user experience. It is additionally noteworthy that we did not approve changes automatically but always read through the code and made sure that the it works as intended before adding it to the codebase. 

---

## Challenges & pivots
> "Where did AI struggle? How did you course-correct?"

There were mainly two challenges to the development with AI: 

* At one point AI suggested to modify files in the Thymia repo. However we wanted to be able to run the code independently of local changes made to the repository. So to pivot we reiterated on the prompt and overall approach to make it more resilient to make our code more robust and modularly independent. 
* Early on, we sometimes overused AI-generated code without fully understanding it, which made debugging difficult. We addressed this by being more intentional with prompts and verifying outputs step by step while focusing on code understanding. Additionally we incorporatied manual checks. This greatly strengthened our understanding of the underlying conceptual code logic which helped us a lot in debugging effectivly.