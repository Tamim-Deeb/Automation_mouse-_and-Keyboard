# Research: UI Polish & Visual Enhancement

## Decision 1: tkinter Theme Engine

**Decision**: Use `ttk.Style` with the "clam" theme as the base, combined with `style.configure()` and `style.map()` for custom colors and hover effects.

**Rationale**: The native OS themes (aqua on macOS, vista on Windows) enforce system colors and ignore custom background settings. The "clam" theme is the most customizable cross-platform ttk theme — it allows full control over background, foreground, border colors, and state-based styling (hover, pressed, disabled). Switching to "clam" unlocks all the styling capabilities needed for the two-tone dark-header/light-content design.

**Alternatives considered**:
- **CustomTkinter**: Modern widgets with rounded corners and transparency, but adds a heavy third-party dependency and changes the widget API. Overkill for this scope.
- **ttkbootstrap**: Bootstrap-style themes, but also adds a dependency and may conflict with existing condition step coloring logic.
- **Direct tk.Widget configure**: Works for Listbox (which is tk, not ttk) but doesn't support hover states. Not sufficient alone.

**Key patterns**:
- `style.theme_use('clam')` at app startup
- `style.configure('Dark.TFrame', background='#2b2b2b')` for dark areas
- `style.map('Custom.TButton', background=[('active', '#hover_color')])` for hover
- `listbox.itemconfig(index, bg=color)` for Listbox rows (tk widget, not ttk)

---

## Decision 2: Dialog Centering Approach

**Decision**: Center dialogs on screen using `winfo_screenwidth/height` after calling `update_idletasks()` to ensure geometry is computed.

**Rationale**: `update_idletasks()` forces tkinter to process pending layout calculations, making `winfo_reqwidth/reqheight` return accurate values. Without it, dialogs may be positioned incorrectly because their size hasn't been computed yet. Centering on screen (not parent window) is preferred because the user specifically wants dialogs not to obscure coordinate-picking areas.

**Alternatives considered**:
- **Center on parent window**: Would keep dialogs near the app, but could obscure the workflow panel or coordinate targets.
- **Remember last position**: Adds complexity without clear benefit for this use case.

**Pattern**:
```python
dialog.update_idletasks()
x = (dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) // 2
y = (dialog.winfo_screenheight() - dialog.winfo_reqheight()) // 2
dialog.geometry(f'+{x}+{y}')
```

---

## Decision 3: Step Highlight Animation

**Decision**: Use `listbox.after()` with a simple two-step color pulse — set highlight color immediately, schedule return to base color after 500ms.

**Rationale**: The `after()` method is non-blocking and thread-safe (runs in tkinter's event loop). A simple two-step pulse (highlight → base) is sufficient for drawing attention without complex multi-frame animation. The base color must account for condition step governance (blue/yellow rows should return to their condition color, not white).

**Alternatives considered**:
- **Multi-frame smooth fade**: 6+ steps with 80ms intervals. Visually smoother but adds complexity and may interact poorly with condition recoloring.
- **Canvas-based overlay**: More control but requires replacing the Listbox widget entirely.

**Pattern**:
```python
def highlight_new_step(listbox, index, base_color='white'):
    listbox.itemconfig(index, bg='#90EE90')  # Light green highlight
    listbox.after(500, lambda: listbox.itemconfig(index, bg=base_color))
```

---

## Decision 4: Limitations & Scope Boundaries

**Decision**: Accept tkinter's visual limitations — no rounded corners, drop shadows, gradients, or opacity transitions. Focus on what tkinter does well: colors, fonts, spacing, and geometry.

**Rationale**: The spec explicitly states "do not change base functions" and the application uses standard tkinter throughout. Introducing CustomTkinter or canvas-based custom widgets would risk breaking existing functionality and add significant complexity. The two-tone color theme, proper sizing, centering, hover effects, and step highlight are all achievable with standard tkinter/ttk.

**What IS possible**:
- Custom background/foreground colors via ttk.Style
- Button hover effects via style.map with 'active' state
- Listbox per-row coloring via itemconfig
- Dialog centering via geometry calculation
- Timer-based animation via after()
- Font sizing and padding adjustments

**What is NOT possible** (and excluded from scope):
- Rounded corners on widgets
- Drop shadows
- Gradient backgrounds
- Smooth opacity/fade transitions
- Custom widget shapes
