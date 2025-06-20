# JackCompiler
Multi-tier compiler for the Jack programming language.

## Context 
Some time ago, I completed the excellent [nand2tetris](https://www.nand2tetris.org/). In this project-led course, the student designs a 16-bit computer, Hack, before programming a software hierarchy that sits atop of this hardware. The end goal is to have Jack code run on Hack. Jack is a simple, Java-like object oriented language, designed by the authors of the course. 

The full Jack compiler:

1. translates Jack code to a stack-based virtual machine language;
2. translates this virtual machine language to Hack's native assembly code; 
3. translates Hack assembly into Hack binary.

I wrote the compiler without knowing any development best practises. Having now completed a data engineering bootcamp at [Northcoders](https://www.northcoders.com/), I couldn't stand to have the compiler public, in its amateurish incarnation! So, I am starting afresh: completely redesigning the compiler, following TDD, writing documentation, and so forth. It's a good opportunity to practise these essential skills, and to remind myself of what I'd learnt about compiler design, and the software/hardware interface.

## State of the Project

This is very much a work in progress, and will probably remain as such for a little while. Currently, the assembler, which handles stage 3 of the compilation process, is part written. I've decided to make it a single pass assembler, rather than the recommended two-passer, for an extra challenge.