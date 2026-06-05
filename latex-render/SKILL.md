---
name: latex-render
description: Render LaTeX formulas to PNG images for Discord display. ONLY use this skill when sending formulas to Discord where LaTeX won't render. DO NOT use for writing files (Obsidian notes, Markdown, etc.) — those support native LaTeX via $$...$$ or $...$ delimiters. This skill converts LaTeX to images for platforms that don't support rendering.
---

# LaTeX Renderer

Convert LaTeX formulas to PNG images **for Discord display only**.

## Step 0: 读取共享配置

先读取 `../_shared/user-config.json`，如果 `../_shared/user-config.local.json` 存在，再用它覆盖默认值。

显式生成并在后续统一使用这些变量：

- `LATEX_CACHE_PATH` — LaTeX 图片缓存目录

## ⚠️ When to Use (Discord Only)

Use this skill when:
- Sending formulas in Discord messages
- User wants to see a formula rendered in chat

## ❌ When NOT to Use

Do NOT use this skill when:
- Writing Obsidian notes (use native `$$...$$` LaTeX)
- Writing Markdown files (use native LaTeX)
- Creating learning notes in Learning/ folder
- Any file-based content (files support LaTeX natively)

**Rule of thumb**: If you're writing to a file, use native LaTeX. If you're sending to Discord, use this skill to render as image.

## Storage Location

All rendered images are saved to `{LATEX_CACHE_PATH}` (from config).

This folder is periodically cleaned by a cron job.

## Usage

### Automatic Render (Preferred)

Write LaTeX using `$$...$$` delimiters:

```
The integral is $$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$
```

Call the script (output defaults to latex-cache):

```bash
python3 scripts/render_latex.py "<latex_code>"
```

Image saved to: `{LATEX_CACHE_PATH}/formula_<timestamp>.png`

### Direct Render

```bash
python3 scripts/render_latex.py '\int_{0}^{\infty} e^{-x^2} dx'
```

### Custom Output (Optional)

```bash
python3 scripts/render_latex.py "<latex>" --output /custom/path.png
```

## Supported LaTeX

- Basic math: fractions, exponents, subscripts
- Integrals: `\int`, `\oint`, limits
- Greek letters: `\alpha`, `\beta`, `\gamma`, etc.
- Symbols: `\sum`, `\prod`, `\sqrt`, `\frac`
- Matrices: `\begin{matrix}...\end{matrix}`
- Advanced: `\mathbb`, `\mathcal`, `\mathbf`

## Example Formulas

| Formula | LaTeX Code |
|---------|------------|
| ∫₀^∞ e^{-x²} dx | `\int_{0}^{\infty} e^{-x^2} dx` |
| ∑ₙ₌₁^∞ 1/n² | `\sum_{n=1}^{\infty} \frac{1}{n^2}` |
| ∇×E = -∂B/∂t | `\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}` |

## Workflow

1. Detect `$$...$$` in your message or user's request
2. Extract LaTeX code
3. Run `render_latex.py` to generate image (saved to latex-cache)
4. Send image via Discord using `message` tool with `media` parameter

## Cache Cleanup

Images are automatically cleaned daily at 3:00 AM (Asia/Shanghai):
- Files older than 24 hours are deleted
- Manual cleanup: `./scripts/clean_latex_cache.sh [hours]`
