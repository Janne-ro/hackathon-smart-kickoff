# How we build

This file aims to show how we worked with AI, not just what we built.

## Planning 
> "How did you use AI to plan your architecture, break down tasks, or explore approaches?"

Initially, we brainstormed ideas ourselves starting with branching out in different directions and then collectivly iterated on them and narrowed down to one final idea we all agreed on.  

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
How did you verify AI-generated code? Did you use test-driven development, manual testing, or AI-assisted debugging?

---

## Challenges & pivots
Where did AI struggle? How did you course-correct?