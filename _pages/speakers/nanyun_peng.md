---
title: Keynote Speaker
layout: single
permalink: /speakers/nanyun_peng/
sidebar:
    nav: "speakers"
classes: wide
---

## August 4 (Tuesday)

{% include keynotes.html
   name="Nanyun (Violet) Peng"
   picture="/assets/images/people/nanyun_peng.jpg"
   site="https://violetpeng.github.io"
   title="Associate Professor of Computer Science"
   institution="University of California, Los Angeles"
   talkinfo="Location: White Hall 208, Time: 9:00 AM"
%}

Dr.  Nanyun (Violet) Peng is an Associate Professor of Computer Science at the University of California, Los Angeles, currently on sabbatical, and a Senior Staff Research Scientist at Google. Her research focuses on controllable language generation, multilingual and multimodal models, and automatic evaluation metrics, with a strong commitment to advancing creativity of AI models. Her work has been recognized with multiple paper awards, including three Outstanding Paper Awards at EMNLP 2024, an Outstanding Paper Award at NAACL 2022, Oral Papers at NeurIPS 2022 and ICML 2023, as well as several Best Paper Awards at workshops. Her research has received support from the NSF CAREER Award, NIH R01, DARPA, IARPA, and multiple industrial research awards. She served as Program Chair for ICLR 2025 and EMNLP 2025, and as a board member of NAACL.

<h2>David and Goliath: Compute-Efficient Strategies for LLM Steering</h2>

Large language models (LLMs) have achieved remarkable capabilities through massive scaling and extensive preference alignment. Yet, the prohibitive computational cost of training, aligning, and controlling these models remains a fundamental challenge. Overcoming this barrier is essential to democratize LLM development, enabling the broader research community to ensure robust safety and factual reliability without relying on resource-heavy retraining pipelines. In this talk, I present our explorations into lightweight, compute-efficient interventions across distinct architectural levels. We demonstrate that because alignment training often induces only small, directional parameter shifts, we can mathematically extrapolate these weights to boost alignment performance without additional training steps. Complementing this parameter-level insight, we investigate the LLM representation space, showing how directed optimization can nudge query representations toward safe, "higher-refusal" directions to prevent harmful compliance. We extend this mechanistic control to the internal routing of Mixture-of-Experts (MoE) architectures, illustrating how inference-time expert activation and deactivation can reliably dictate high-level behaviors like factual faithfulness and safety. Taken together, these directions sketch a roadmap toward highly steerable language models—systems that can be efficiently adapted, safeguarded, and refined within constrained computational budgets.

[[slides]](/assets/files/presentations/Keynote-Nanyun_Peng.pdf)