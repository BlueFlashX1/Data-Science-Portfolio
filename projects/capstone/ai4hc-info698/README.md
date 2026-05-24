# AI4HC Capstone: ER Simulator Showcase Poster

[![Course Project](https://img.shields.io/badge/Course-Capstone-blue?style=for-the-badge)](https://arizona.edu)
[![INFO 698](https://img.shields.io/badge/INFO%20698-Graduate%20Capstone-red?style=for-the-badge)](https://arizona.edu)
[![University of Arizona](https://img.shields.io/badge/University%20of-Arizona-navy?style=for-the-badge)](https://arizona.edu)

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![Information Design](https://img.shields.io/badge/Information-Design-purple?style=flat-square)

> Healthcare AI training simulator, built by a 6-person team capstone. My role was the showcase poster and the avatar source footage. University of Arizona, INFO 698, Spring 2026.

**View the live poster:** [light theme](https://blueflashx1.github.io/Data-Science-Portfolio/projects/capstone/ai4hc-info698/index_v1.html) · [dark theme](https://blueflashx1.github.io/Data-Science-Portfolio/projects/capstone/ai4hc-info698/index_dark.html) · [print PDF](./iShowcase_Final.pdf)

**Team codebase:** [UA-AICore/Emergency-Room-Simulator-Repository](https://github.com/UA-AICore/Emergency-Room-Simulator-Repository)

The poster (polished from Abhiram Varma Nandimandalam's initial HTML draft at [isjustabhi/AI4HC](https://github.com/isjustabhi/AI4HC)) and the print-export pipeline I authored are in this folder.

---

## What This Was

A 6-person team capstone for the UofA AI Core, building an AI-powered training simulator for emergency-room learners. The team product is a .NET 8 web app with a RAG-backed chat tutor over a medical knowledge base, a HeyGen streaming avatar, and a multiple-choice quiz generator.

I wasn't on the engineering side. My job on this team was design and the avatar source.

---

## My Contributions

**1. The showcase poster.**

- Took Abhiram Varma Nandimandalam's initial HTML draft ([isjustabhi/AI4HC](https://github.com/isjustabhi/AI4HC)) and polished it into the team's final capstone poster (layout, theme variants, CSS iteration)
- HTML/CSS source so we could iterate in a browser; exported to a 4×3 ft print-ready PDF via [`scripts/export_poster.py`](./scripts/export_poster.py), a Python pipeline I wrote that renders the HTML in headless Chrome at 4608×3456 px, screenshots it, and embeds the PNG losslessly into a 48×36 in PDF with print-shop metadata
- The team printed from this PDF for the iShowcase event and the physical poster came out matching the on-screen render exactly
- Two variants: a light version for the project slide demo, a dark version for the printed banner
- Summarizes the team's system in one visual: the RAG pipeline, the avatar integration, the quiz engine, the learner flow
- View live: [light theme](https://blueflashx1.github.io/Data-Science-Portfolio/projects/capstone/ai4hc-info698/index_v1.html) · [dark theme](https://blueflashx1.github.io/Data-Science-Portfolio/projects/capstone/ai4hc-info698/index_dark.html). Or [`iShowcase_Final.pdf`](./iShowcase_Final.pdf) for the print version.

**2. Avatar source footage.**

- Recorded the 1-minute source clip of myself for the team's HeyGen avatar
- Handed the footage to the project coordinator, who handled the HeyGen API wiring
- I didn't write that integration code; my contribution was being the source

That's it. The codebase, the RAG service, the API integration, and the quiz engine were all teammate work.

---

## Project Structure

```text
ai4hc-info698/
├── README.md                           # Project documentation
├── index_v1.html                       # Poster source, unified version (open in a browser to render it as displayed)
├── index_dark.html                     # Earlier dark-theme variant of the poster source
├── iShowcase_Final.pdf                 # Final printed showcase poster (3.2MB)
├── AI4HC_poster_dark.pdf               # Dark-theme variant of the print PDF (3.6MB)
├── system_workflow.png                 # System architecture diagram embedded in the poster
├── qr-final-codira.png                 # QR code from the poster (links to the live demo)
├── UA_logo.svg                         # UA branding asset (referenced by both HTML variants)
└── scripts/
    └── export_poster.py                # Headless Chrome + img2pdf pipeline rendering HTML to 48×36 in print-ready PDF
```

---

## What I Didn't Build

To be explicit: the .NET web app, the RAG service backed by the medical knowledge base, the HeyGen streaming avatar integration, and the multiple-choice quiz engine were all built by the engineering members of the team (Ameya, hginman, hcp62, and others). My only contribution to the codebase side was the avatar source recording. The poster and its build pipeline are mine; the rest isn't.

---

## Tech Stack

HTML • CSS • Python (headless Chrome → img2pdf print pipeline) • Information design • Technical communication
