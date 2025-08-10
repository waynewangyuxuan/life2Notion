# Development Regulations

This document outlines the core principles that I, the AI assistant, must follow during the development of the `Life2Notion` project. These rules ensure the codebase is maintainable, scalable, and easy to navigate.

## 1. Principle of Atomicity
This is the foundational principle of our project. It applies to both file structure and code.

### 1.1. Atomic File Structure
- Each file should have a single, well-defined purpose.
- A file that defines a server should only define the server. A file that contains utility functions should only contain those functions.
- Avoid creating monolithic files that handle multiple, unrelated responsibilities.

### 1.2. Atomic Code (Functions/Classes)
- Every function or class should do one thing and do it well.
- Functions should be small and focused. If a function is performing multiple distinct operations, it should be broken down into smaller, more specific functions.
- This principle promotes reusability and simplifies testing and debugging.

## 2. Principle of Co-located Documentation
To ensure that the project remains understandable and that the purpose of complex components is clear, we will adhere to the following documentation rule.

- Any significant feature, module, or service within a package must be accompanied by a `.md` file in the same directory.
- This file should explain the feature's purpose, its core logic, and how it interacts with other parts of the system.
- **Example**: If we create a complex `PropertyRecommender` service within the `agent` package, it must be located alongside a `PropertyRecommender.md` file that explains its algorithm and usage.