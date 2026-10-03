# 5-day-ai-agents-intensive-vibecoding-course-with-google

- 类别：Featured ｜ 主题：other ｜ 子类：meta ｜ 领域：—
- 截止：2026-06-19 ｜ 队伍数：0 ｜ 机制：标准赛
- 评估指标：
- 讨论区：11 条主题

## 讨论区索引（按票数排序）

- 4217 票 / 0 评论 | 🎒 Day 1  Assignment  
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708280
- 2592 票 / 0 评论 | [Welcome + Setup Instructions] 5-Day AI Agents: Intensive Vibe Coding Course With Google  
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708114
- 2147 票 / 0 评论 | 🎒 Day 2 Assignment 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708469
- 1654 票 / 0 评论 | Codelabs FAQs 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708107
- 1564 票 / 0 评论 | 🎒 Day 3 Assignment 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708744
- 1254 票 / 0 评论 | 🎒 Final Assignment 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/709464
- 1232 票 / 0 评论 | 🎒 Day 4 Assignment 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/709165
- 655 票 / 0 评论 | [Capstone Project] 5 Days AI Agents: Intensive Vibe Coding Course With Google 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/709721
- 609 票 / 0 评论 | [Wrap Up + Next Steps] 5-Day AI Agents: Intensive Vibe Coding Course With Google 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/709712
- 306 票 / 0 评论 | [Learn Guide] 5-Day AI Agents: Intensive Vibe Coding Course With Google 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/716539
- 82 票 / 0 评论 | Thank you for Making the 5-Day AI Agents: Vibe Coding Intensive a Success! 
  https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/730957

## write-up 正文（6 篇）

### Codelabs FAQs

来源：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708107

1. About Cost

1.1. Is there a cost to take this course?

No, this is a no-cost course. There is no course fee, and the curriculum, labs, whitepapers, livestreams, recordings, and Discord community are all included at no cost.

Due to capacity limitations, you may find that it may take longer than the 5 days to complete all codelabs. We recognize that this could be a frustrating experience, so to ensure everyone has an opportunity to get the most out of this course we are doing the following: 

The badge and certificate for this course will be awarded based on participation in the capstone project. Completion of all codelabs is not a prerequisite to receive the badge or certificate - you can complete at your own pace. 

Kaggle will continue support on the Kaggle Discord with experts for two weeks after the course concludes. We've set up dedicated channels for event discussions and learnings. For anyone who wants to work through their codelabs after capacity limits have reset. Feel free to bring questions to those channels and connect with other learners. 

1.2. What about deployment - doesn't deploying to Google Cloud require billing?

The course includes deployment in two places, and the setup requirements differ between them.

Day 1: Deploy from AI Studio to Cloud Run (no billing account required).
The Day 1 deployment uses the Google Cloud Starter Tier, which lets you publish up to two full-stack applications without setting up a Google Cloud project or billing account. For details including eligibility for the Starter Tier, see the official guide: Deploying your app to Cloud Run from AI Studio.

Day 5: Deploy agents to Cloud Run and Agent Runtime (optional, requires a billing account). 
The Day 5 hands-on deployment lab is optional and uses a different setup that requires a Google Cloud project with billing enabled. For product-level pricing details, including their free tiers, see the Cloud Run pricing page and the Agent Runtime pricing page. There are supported paths for every learner:

Hands-on with the Google Cloud Free Trial: New users can activate the Google Cloud Free Trial, which includes $300 in credit - far more than enough for the Day 5 lab.

Hands-on with an existing billing account: To minimize any potential costs, shut down and delete any resources as soon as you are done with the codelabs.

Read-along path: Follow the Day 5 lab by reading through it and watching the livestream walkthrough. You'll still learn the concepts, the architecture, and what the deployment looks like end-to-end.

Any of these paths is a valid way to complete the course, with no penalty or missed certificate requirement.

1.3. I've already used my $300 Google Cloud trial credit from a previous course - can I still take this one?

Yes, absolutely. The $300 credit is a nice-to-have for the optional Day 5 hands-on deployment, but it is not required to take the course or to complete it. 

If you've already used your credit, see the alternatives listed under Day 5 in 1.2 - including the read-along path. And Day 1's deployment uses the Google Cloud Starter Tier, which doesn't require billing. 

1.4 If I do choose to deploy on Day 5, how do I make sure I don't get surprise charges?

If you opt in to the hands-on deployment path, a few simple steps keep your spend at essentially zero:

Clean up when you're done. Delete the Cloud Run services and Agent Runtime deployments you created. Deleting the entire Google Cloud project is the cleanest, most complete way to remove everything.

Delete any API keys you created, even if you never enabled billing. This is good practice regardless.

Confirm billing is shut off in the Cloud Console once you've finished.

We'll include step-by-step cleanup instructions at the end of the relevant labs.

2. Prerequisites & Setup

2.1 What technical prerequisites do I need?

Python familiarity is helpful, but for much of the course you won't need heavy coding skills — a lot of the code is generated for you through Antigravity, MCP servers, and Skills.

Comfort with the command line (terminal / shell) is ideal.

A rough understanding of what LLMs are is helpful. If you're brand new to LLMs, the previous Kaggle 5-Day Gen AI Intensive Course with Google is a great primer.

2.2 What accounts and tools do I need to set up before Day 1?

You'll need the following:

Kaggle account

Google account (for AI Studio)

Google AI Studio API key

Discord (community)

Google Antigravity (IDE) installed locally

Agents CLI installed locally

Optional (only for the hands-on Day 5 deployment path): a Google Cloud project.

2.3 How do I get a Gemini API key?

Follow the official guide: Get a Gemini API key. This same key works for building agents with ADK.

Store it securely: for example, in an environment variable or a secrets manager.

Never commit keys to public notebooks or repos. 

3. Course Format & Products

3.1 What Google products will I use across the 5 days?

Day
Product(s)
Purpose

1
Antigravity 2.0, IDE + CLI, AI Studio, Cloud Run
Visual + headless vibe coding; deploy first app

2
Antigravity IDE, MCP servers, Skills
Extend Antigravity with external tools and reusable skills

3
Agents CLI, ADK
Manage agent lifecycle, generate UIs

4
ADK 2.0, Agents CLI, Antigravity 2.0
Build graph-based ambient agents; secure development

5
Agents CLI, Agent Runtime, Cloud Run, Antigravity IDE
Deploy agents to production

3.2 Do I need to install anything locally?

Yes. Unlike previous Kaggle intensives, this course requires local installs (Antigravity IDE, Antigravity CLI, Python dependencies). Plan some setup time before Day 1.

4. Google Antigravity

4.1 What is Google Antigravity and why does the course use it?

Google Antigravity is an agentic AI IDE and CLI from Google. It's central to this course because it powers both the visual and headless "vibe coding" workflows you'll use across all 5 days.

New to Antigravity? Start with the official Getting started guide. For product-level details including age and region eligibility - see the Antigravity FAQ.

4.2 How do I install Antigravity? Is there a cost? Which OSes are supported?

Antigravity is available at no cost for individuals when used with your Google account - see the Antigravity pricing page for details.

It runs on macOS, Linux, and Windows.

Install links: Antigravity IDE, Antigravity 2.0, and Antigravity CLI.

For eligibility (age, region) and other product-level questions, see the official Antigravity FAQ.

4.3 What are the system requirements?

We'll publish exact RAM, CPU, disk, and network requirements in the Day 0 setup guide. As a rule of thumb, any modern laptop that can comfortably run a typical IDE (such as VS Code) will be sufficient for the labs.

4.4 I've run out of quota in Antigravity. What can I do?

Antigravity offers leading frontier models from Google. You can change models if you have quota in other models. If you are out of quota, you have a few options:

Wait until your quota resets

Upgrade to a paid tier (see Antigravity pricing)

For those who are completing the course using the free tier tools, we understand that these codelabs may require more capacity than is given free for the week. There is no completion deadline for the codelabs - you can wait for your quota to refill and complete these in your own time. This will not affect your eligibility for a badge or certificate for the course.

5. Local vs. Cloud Labs

Important: This course is not notebook-based and not Colab-based. Most labs run in the Antigravity IDE / Antigravity CLI on your local machine.

5.1 Which labs run locally vs. in the cloud?

Local (Antigravity 2.0 / Antigravity CLI): Days 1, 2, 3, 4, and the build phase of Day 5

Cloud (deployment):

Day 1: deploy to Cloud Run via the Google Cloud Starter Tier (no billing account required)

Day 5: optional hands-on deployment to Cloud Run and Agent Runtime (requires a billing account; see question 1.2)

5.2 Can I run any of the materials in Kaggle Notebooks or Colab?

The course materials are not designed for Kaggle or Colab.

6. Getting Help

6.1 Where do I ask questions during the course?

Kaggle Discord has dedicated channels for event discussions and learnings.

---

### [Welcome + Setup Instructions] 5-Day AI Agents: Intensive Vibe Coding Course With Google 

来源：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708114

Welcome to our 5-Day AI Agents: Intensive Vibe Coding Course With Google!

Here’s a brief summary of how the course works and detailed instructions on how to get set up. You’ll receive your first assignment on Sunday, June 14, 2026.

How the Course Works

The course is designed to be flexible and interactive, allowing you to learn at your own pace while benefiting from live sessions and community engagement.

Daily Content Release: New assignments will be posted in here each day, your primary source for all course materials.

Assignment Notifications (Fast Follow): Given the large number of participants, links to all assignment materials including whitepapers, codelabs and podcast episodes will also be shared on the Kaggle Discord and sent via follow-up email shortly after being posted. You can find the codelabs FAQs here. 

Support & Discussion: Join the discussion on our dedicated Discord channels to connect with other learners, ask questions, and get support from Google researchers and engineers who’ll be monitoring the channels throughout the week.

Daily Livestreams: Join Anant Nawalgaria and Smitha Kolan live each day starting Monday, June 15th at 11 AM PT / 8 PM CET / 11:30 PM IST on Kaggle’s YouTube channel. They’ll be joined by special guests from Google. After each session, recording links will be shared in Kaggle's Discord.

Course Completion: To get the most out of this intensive, we recommend completing all course materials including whitepapers, podcasts and codelabs at your own pace. 

[Optional] Capstone Project: On the final day, you’ll have the chance to apply everything you’ve learned by building your own AI agent. By participating in the capstone project, you’ll earn a badge and certificate on Kaggle.

AI Agents Intensive November 2025 Update: The whitepapers are now updated in last year’s 5-Day AI Agents Intensive Course with Google Learn Guide. 

Setup Instructions

To ensure you’re ready for the course, please complete these essential setup steps:

Kaggle Account: Sign up for a Kaggle account. 

AI Studio Account: Sign up for an AI Studio account and ensure you can generate an API key.

Download and install: 

Antigravity 2.0

Antigravity IDE

Antigravity CLI

Kaggle Discord: Sign up for a Discord account and join us on the Kaggle Discord server . We've set up dedicated channels for event discussions and learnings.

Please note that if you’d like to post on other channels on the Kaggle discord you’ll need to link your Kaggle account to discord here.

Once you have everything set up, please introduce yourself in the #5dgai-introductions channel on Discord. 

We’re looking forward to meeting you!
AI Agents Intensive November 2025 Update: The whitepapers are now updated in last year’s 5-Day AI Agents Intensive Course with Google’s Learn Guide.

---

### 🎒 Final Assignment

来源：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/709464

We've reached the final assignment! 🎉

Complete Unit 5 - "Spec-Driven Production Grade Development in the Age of Vibe Coding":

Listen to the summary podcast episode for this unit.

To complement the podcast, read the "Spec-Driven Production Grade Development in the Age of Vibe Coding" whitepaper.
Complete these codelabs:

[Optional] Deploy and host your AI agents on Google Cloud

[Optional] Build a front-end web app and link it to your cloud-hosted AI agent

💡 What You'll Learn

Today's whitepaper covers bridging the gap between fragile vibe-coded prototypes and production-grade enterprise software using Spec-Driven Development (SDD). It details how to treat code as disposable and behavior-driven Gherkin specifications as the source of truth, establishing safe, zero-trust development pipelines with automated code-review agents and hybrid Policy Servers.

In the codelabs, you will learn how to create and deploy an agent to Google Cloud for enterprise scale. Then you will use Antigravity to vibe code a frontend client interface deployed to Cloud Run and tie it to an asynchronous event-triggering architecture that automatically feeds live expense submissions straight to your cloud-hosted agent. While these codelabs are optional today because they may require a billing account on Google Cloud, we still encourage you to scan through them to familiarize yourself with what productionization of agents and apps might look like at enterprise scale.

📋 Reminders and Announcements

Find a complete list of scheduled livestreams and past recordings here.

The final livestream is tomorrow at 11 AM PT.

Anant Nawalgaria and Smitha Kolan will be joined by codelabs author Lavi Nigam, and special guests from Google: Ankur Jain, Antonio Gulli, Elia Secchi, Lee Boonstra, and Omar Sanseviero.

As a reminder, you don’t need to submit any outputs from the assignments. You can complete them at your own pace.

Be sure to ask all your questions about the podcast, readings, and codelabs in the #5dgai-question-forum channel on Kaggle's Discord, where other participants and Googlers are ready to help. Questions selected from Discord for discussion during the livestream will be chosen for Kaggle swag!

We want this community to be positive and supportive. Please follow Kaggle's community guidelines found here.

Happy learning and see you tomorrow!

---

### 🎒 Day 2 Assignment

来源：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708469

Complete Unit 2 – “Agent Tools & Interoperability”

Listen to the summary podcast episode for this unit.

To complement the podcast, read the "Agent Tools & Interoperability" whitepaper.

Complete these codelabs:

Get started with Antigravity CLI

Explore Google Developer Knowledge MCP server in Google Antigravity

💡 What You'll Learn

Today's whitepaper talks about standardizing the plug-and-play AI ecosystem using open protocols to eliminate the complex technical debt of custom tool integrations. It details how the Model Context Protocol (MCP) connects models to data sources, outlines Agent2Agent (A2A) collaboration, showcases Agent-to-User Interface (A2UI) for generative UI, and introduces Agent Payments Protocol (AP2) and Universal Commerce Protocol (UCP) for secure machine-to-machine commerce.

In today's codelabs, you'll learn how to add MCP servers to Antigravity, giving it access to the canonical, machine-readable source of Google's public developer documentation. You'll then extend your familiarity with Antigravity by using it via the terminal with Antigravity CLI.

📋 Reminders and Announcements

We experienced a technical issue with our livestream timing this morning and apologize for the inconvenience. You can find day 1 livestream recording here.

In tomorrow's livestream at 11:00 AM PT, Anant Nawalgaria and Smitha Kolan will be joined by codelabs author Fran Hinkelmann, along with other special guests from Google: Mike Clark, Alan Blount, Kanchana Patlolla, and Pier Paolo Ippolito.

As a reminder, you don't need to submit the assignments. You can complete them at your own pace.

Be sure to ask all your questions about the podcast, readings, and codelabs in the #5dgai-question-forum channel on Kaggle's Discord, where other participants and Googlers are ready to help. Questions selected from Discord for discussion during the livestream will be chosen for Kaggle swag!

We want this community to be positive and supportive. Please follow Kaggle's community guidelines found here.

Happy learning and see you tomorrow!

---

### 🎒 Day 3 Assignment

来源：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708744

Complete Unit 3 - "Agent Skills":

Listen to the summary podcast episode for this unit.

To complement the podcast, read the "Agent Skills" whitepaper: https://www.kaggle.com/whitepaper-agent-skills

Complete these codelabs:

Explore how Skills work in Antigravity

Build agents in Antigravity with Agents CLI and ADK

💡 What You'll Learn

Today's whitepaper talks about managing dynamic context and avoiding "context rot" by equipping agents with portable "Agent Skills", directories structured around a central SKILL.md file. It explains how this framework uses progressive disclosure to keep system prompts lightweight, loading execution details and tools only on demand so that single agents can flex into hundreds of specialist roles efficiently.

In the codelabs, you will familiarize yourself with skills in Antigravity. Then, using Antigravity, you will install and use Agents CLI skills to create agents, lint your code, and test your agent, all by using natural language prompts.

📋 Reminders and Announcements

Find a complete list of scheduled livestreams and past recordings here.

The next livestream is tomorrow at 11 AM PT / 8 PM CET / 11:30 PM IST.

Anant Nawalgaria and Smitha Kolan will be joined by codelabs author Polong Lin along with guests from Google: Debanshu Das, Gabriela Hernandez Larios, Julia Wiesinger, and Tanvi Singhal.

As a reminder, you don't need to submit any outputs from the assignments. You can complete them at your own pace.

Be sure to ask all your questions about the podcast, readings, and codelabs in the #5dgai-question-forum channel on Kaggle's Discord, where other participants and Googlers are ready to help. Questions selected from Discord for discussion during the livestream will be chosen for Kaggle swag!

We want this community to be positive and supportive. Please follow Kaggle's community guidelines.

Happy learning and see you tomorrow!

---

### 🎒 Day 1  Assignment 

来源：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708280

Complete Unit 1 – "Introduction to Agents & Vibe Coding"

Listen to the summary podcast episode for this unit.

To complement the podcast, read "The New SDLC with Vibe Coding" whitepaper.

Complete these codelabs:

Get started with Antigravity 2.0 and IDE

Build a Web Application in AI Studio and Deploy to Cloud Run

💡What You'll Learn

Today's whitepaper talks about the transition from manual syntax coding to intent-driven "vibe coding" and disciplined "agentic engineering." It explores how AI agents compress the traditional software development life cycle (SDLC) and explains the "factory model" where developers act as system orchestrators who design the evaluation, constraint, and context harnesses that safely guide autonomous execution.

In the codelabs, you'll familiarize yourself with Antigravity 2.0, the Antigravity IDE, and the Antigravity CLI to vibecode your first applications. You'll also use Google AI Studio to deploy your app to Cloud Run, enabling you to share your vibe coded app with your friends.

📋 Reminders

Tomorrow at 11:00 AM PT, Anant Nawalgaria and Smitha Kolan will host the first livestream on Kaggle's YouTube channel. They'll be joined by codelabs author Fran Hinkelmann, along with other special guests from Google: Jamie de Guerre, Logan Kilpatrick, Parthasarathy Ranganathan, and Shubham Saboo to discuss the assignments and share insights.

We want this community to be positive and supportive. Please follow Kaggle's community guidelines found here.

Happy learning and see you tomorrow!

---
