This `GEMINI.md` outlines the specific coding principles and practices for the `vollwerk` subproject, building upon the [General Coding Principles](../../GEMINI.md) established at the root of the repository.

## 1. Test-Driven Development (TDD) for Web Projects

For the `vollwerk` project, TDD will focus on:
-   **Unit Testing:** JavaScript functions and modules should have dedicated unit tests to ensure individual components work as expected. We will identify appropriate JavaScript testing frameworks (e.g., Jest, Mocha) as needed.
-   **Integration Testing:** Verify the interaction between different front-end components and potentially with mocked backend APIs.
-   **End-to-End Testing:** For critical user flows, we will implement end-to-end tests using tools like Cypress or Playwright to simulate user interactions in a browser.
-   **Visual Regression Testing:** Consider using tools to detect unintentional visual changes in the UI, especially important for a landing page project.

## 2. `vollwerk` Project Standards & Production Readiness

In addition to the general professional standards, `vollwerk` will adhere to:
-   **Semantic HTML5:** Use appropriate HTML5 elements for structure and meaning.
-   **Responsive Design:** Ensure the website is fully responsive and accessible across various devices and screen sizes.
-   **CSS Best Practices:** Utilize SASS for modular, maintainable, and scalable stylesheets. Adhere to naming conventions (e.g., BEM, utility-first where appropriate).
-   **JavaScript Quality:** Write clean, modern (ES6+), and efficient JavaScript. Avoid global variables and prefer modular patterns.
-   **Performance Optimization:**
    -   Optimize images for web (compression, appropriate formats).
    -   Minimize and concatenate CSS and JavaScript files.
    -   Leverage browser caching.
    -   Ensure fast loading times (aim for good Lighthouse scores).
-   **Accessibility (A11Y):** Design and develop with accessibility in mind, following WCAG guidelines.
-   **Cross-Browser Compatibility:** Ensure consistent functionality and appearance across target browsers.

## 3. `vollwerk` Technologies & Tools

The primary technologies and tools for `vollwerk` include:
-   **Markup:** HTML5
-   **Styling:** CSS3, SASS (using `assets/sass` for development)
-   **Scripting:** JavaScript (ES6+), jQuery (as identified in `assets/js/jquery.min.js`)
-   **Build/Automation:** Gulp (for SASS compilation, minification, etc.)
-   **Version Control:** Git (integrated with GitHub)

## 4. `vollwerk` Deployment & CI

-   (Details to be added here once deployment strategy is defined, e.g., static site hosting, CDN integration, automated builds via GitHub Actions/GitLab CI)

---

### Agent's `vollwerk` Optimization Notes:

-   **Current Observation:** The project previously used `jQuery` and `.min.js` files, and a basic SASS compilation.
-   **Optimization Achieved:**
    -   Implemented a Gulp-based build system (`gulpfile.js`) for automated SASS compilation, CSS minification, and JavaScript minification.
    -   Migrated SASS `@import` rules to `@use` rules, adhering to the modern SASS module system.
    -   Refactored SASS files to correctly import dependencies using `@use` in each partial that requires them.
    -   Renamed private SASS utility functions (e.g., `_size`, `_palette`) to public names (e.g., `size`, `palette`) and updated all their call sites.
    -   Fixed various SASS deprecation warnings:
        -   `transparentize()`, `lighten()`, `darken()` replaced with `color.adjust()`.
        -   `@elseif` replaced with `@else if`.
        -   `global-builtin` functions (`type-of`, `nth`, `index`, `str-length`, `str-slice`) replaced with their module-specific counterparts (`meta.type-of`, `list.nth`, `list.index`, `string.length`, `string.slice`).
        -   `slash-div` operations replaced with `math.div()`.
        -   Removed duplicated helper functions from `libs/_vendor.scss`.
    -   Integrated BrowserSync for live reloading during development.
-   **Next Steps for TDD:** Now that the build system is robust, we can proceed with setting up a JavaScript testing framework for unit and integration tests.
-   **Skill Suggestion:** A "Frontend Optimization Skill" could be highly beneficial for this project to automate many of the performance and build-related tasks.
-   **Extension Suggestion:** Consider a VS Code extension for SASS linting and formatting.
