# Ultimate UI/UX Component Library: World-Famous Websites & Tekken 8 Move-List Design System

Yeh document aapki website ya app design karne ke liye ek complete **Design System & Component Blueprint** hai. Ismein duniya ki sabse mashhoor websites (Apple, Linear, Stripe, Riot Games) ke **Buttons, Cards, aur Image Displays** ke sath-sath **Tekken 8** ki official site aur top move-list databases (**Wavu Wiki, TekkenDocs, Okizeme.gg**) ka exact UI breakdown, color codes, aur ready-to-use HTML/Tailwind CSS code shamil hai.

---

## PART 1: TEKKEN 8 & FIGHTING GAME MOVE-LIST UI SYSTEM
*(Inspired by Official Bandai Namco Tekken 8 UI, Wavu Wiki, TekkenDocs & Okizeme)*

Tekken 8 ka UI **"Aggressive Cyber-Brutalism + Dark Glassmorphism"** par bana hai. Ismein sharp angles (skewed boxes), neon magenta/red/cyan glows, aur high-contrast frame data badges use hote hain.

### 1. Tekken 8 Official Color Palette & Typography
| Element | Color Name | Hex Code | Usage |
| :--- | :--- | :--- | :--- |
| **Background Primary** | Void Obsidian | `#090A0F` | Main page background |
| **Card Surface** | Dark Carbon Glass | `#12151F` (85% Opacity) | Move cards, character panels |
| **Primary Accent** | Tekken Crimson / Pink | `#FF0055` to `#D90429` | Active buttons, Heat Engager highlights |
| **Secondary Accent** | Electric Jin Lightning / Cyan | `#00F0FF` | Frame advantage (+ frames), Heat Burst |
| **Warning / Punish** | Kazuya Devil Purple / Gold | `#F59E0B` / `#A855F7` | Tornado, Homing, Wall Crush |
| **Fonts** | Display / Headers | `Tekken`, `Oswald`, `Rajdhani`, or `Bebas Neue` | Bold, uppercase, italicised (`-skew-x-6`) |
| **Data Font** | Frame Numbers | `JetBrains Mono` or `Chakra Petch` | `-14`, `+5`, `i15` (startup frames) |

---

### 2. Tekken 8 Character Roster & Image Display Card (Slanted / Skewed)
Official Tekken 8 website par character cards seedhe (rectangle) nahi hote, balki **`skew-x-[-8deg]`** (tirchay) hote hain, aur jab mouse upar aata hai (hover) toh character ki PNG image card ke border se bahar nikalti hai (**Pop-out 3D Effect**) aur peeche neon bijli (glow) chalti hai.

```html
<!-- Tekken 8 Character Select Card (Tailwind CSS) -->
<div class="group relative w-64 h-80 bg-[#12151F] border-2 border-zinc-800 hover:border-[#FF0055] transform -skew-x-6 transition-all duration-300 hover:scale-105 hover:shadow-[0_0_30px_rgba(255,0,85,0.5)] overflow-hidden cursor-pointer">
  
  <!-- Background Diagonal Grid / Halftone Pattern -->
  <div class="absolute inset-0 bg-[radial-gradient(#ff0055_1px,transparent_1px)] [background-size:16px_16px] opacity-10 group-hover:opacity-30 transition-opacity"></div>

  <!-- Bottom Glow Gradient -->
  <div class="absolute inset-0 bg-gradient-to-t from-[#090A0F] via-transparent to-transparent z-10"></div>
  <div class="absolute -bottom-10 left-0 right-0 h-32 bg-[#FF0055] blur-2xl opacity-0 group-hover:opacity-40 transition-opacity duration-300"></div>

  <!-- Character Cutout Image (Un-skewed slightly so character looks straight) -->
  <img src="https://placehold.co/400x500/12151F/FF0055?text=JIN+KAZAMA" alt="Jin Kazama" 
       class="w-full h-full object-cover transform skew-x-6 scale-105 group-hover:scale-115 transition-transform duration-500 ease-out" />

  <!-- Character Name Banner -->
  <div class="absolute bottom-0 inset-x-0 p-4 z-20 flex flex-col items-start transform skew-x-6">
    <span class="text-[10px] font-mono uppercase tracking-[0.25em] text-[#00F0FF] bg-[#00F0FF]/10 px-2 py-0.5 border border-[#00F0FF]/30 mb-1">
      Mishima Style
    </span>
    <h3 class="text-2xl font-black italic uppercase tracking-wider text-white group-hover:text-[#FF0055] transition-colors">
      JIN KAZAMA
    </h3>
  </div>
</div>
```

---

### 3. Tekken 8 Move-List & Frame Data Card (Wavu Wiki / TekkenDocs Style)
Tekken 8 ki move-list websites (jaise **TekkenDocs**, **Wavu Wiki**, aur **Okizeme.gg**) ki sabse badi khoobi unka **Command Input Visualizer** (Joystick arrows + color-coded attack buttons `1, 2, 3, 4`) aur **Frame Data Pills** hain.

#### Visual Input System Rules (Tekken Standard):
*   **`1` (Left Punch - Square / X):** Blue (`#3B82F6`)
*   **`2` (Right Punch - Triangle / Y):** Yellow/Gold (`#EAB308`)
*   **`3` (Left Kick - Cross / A):** Green (`#22C55E`)
*   **`4` (Right Kick - Circle / B):** Red/Pink (`#EF4444`)
*   **Frame Data Color Coding:**
    *   **Safe on Block (`-9` to `-1`):** Neutral Gray/White (`#9CA3AF`)
    *   **Plus on Block (`+1` or higher):** Electric Cyan/Green (`#10B981` / `#00F0FF`)
    *   **Launch Punishable (`-15` or worse):** Crimson Danger (`#EF4444`)

```html
<!-- Tekken 8 Move List Card Component -->
<div class="w-full max-w-4xl bg-[#11131C] border border-zinc-800/80 hover:border-[#FF0055]/60 rounded-lg p-4 transition-all duration-200 shadow-lg hover:shadow-[0_4px_25px_rgba(255,0,85,0.15)]">
  
  <!-- Top Row: Move Name, Input Notation, and Special Properties (Heat / Tornado) -->
  <div class="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-800/80 pb-3">
    <div>
      <div class="flex items-center gap-2">
        <span class="text-xs font-mono text-zinc-500">#042</span>
        <h4 class="text-lg font-extrabold tracking-wide text-white uppercase">Electric Wind God Fist (EWGF)</h4>
      </div>
      
      <!-- Visual Button Input Notation (f, n, d, df+2) -->
      <div class="flex items-center gap-1.5 mt-2">
        <span class="px-2 py-0.5 bg-zinc-800 text-zinc-200 font-mono text-xs rounded border border-zinc-700">→</span>
        <span class="px-2 py-0.5 bg-zinc-900 text-zinc-400 font-mono text-xs rounded border border-zinc-800">★</span>
        <span class="px-2 py-0.5 bg-zinc-800 text-zinc-200 font-mono text-xs rounded border border-zinc-700">↓</span>
        <span class="px-2 py-0.5 bg-zinc-800 text-zinc-200 font-mono text-xs rounded border border-zinc-700">↘</span>
        <span class="text-zinc-500 font-bold">+</span>
        <!-- Tekken "2" Button (Yellow/Gold Circle) -->
        <span class="w-6 h-6 rounded-full bg-yellow-500 text-black font-black text-xs flex items-center justify-center shadow-[0_0_10px_rgba(234,179,8,0.6)]">
          2
        </span>
      </div>
    </div>

    <!-- Tekken 8 Move Property Badges (Heat Engager, Tornado, Homing) -->
    <div class="flex items-center gap-2">
      <span class="px-2.5 py-1 text-[11px] font-black uppercase tracking-wider bg-[#FF0055]/15 text-[#FF0055] border border-[#FF0055]/40 rounded-sm transform -skew-x-12">
        HIGH (H)
      </span>
      <span class="px-2.5 py-1 text-[11px] font-black uppercase tracking-wider bg-cyan-500/15 text-cyan-400 border border-cyan-500/40 rounded-sm transform -skew-x-12">
        LAUNCHER
      </span>
      <span class="px-2.5 py-1 text-[11px] font-black uppercase tracking-wider bg-orange-500/15 text-orange-400 border border-orange-500/40 rounded-sm transform -skew-x-12">
        🔥 HEAT ENGAGER
      </span>
    </div>
  </div>

  <!-- Bottom Row: Frame Data Grid (Startup, Block, Hit, Counter Hit, Damage) -->
  <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-3 text-center font-mono">
    <div class="bg-[#0B0C12] p-2 rounded border border-zinc-800/60">
      <div class="text-[10px] text-zinc-500 uppercase">Startup</div>
      <div class="text-sm font-bold text-white">i11~14</div>
    </div>
    <div class="bg-[#0B0C12] p-2 rounded border border-emerald-500/30">
      <div class="text-[10px] text-zinc-500 uppercase">On Block</div>
      <div class="text-sm font-bold text-emerald-400">+5 (Pushback)</div>
    </div>
    <div class="bg-[#0B0C12] p-2 rounded border border-cyan-500/30">
      <div class="text-[10px] text-zinc-500 uppercase">On Hit</div>
      <div class="text-sm font-bold text-cyan-400">+59a (Launch)</div>
    </div>
    <div class="bg-[#0B0C12] p-2 rounded border border-purple-500/30">
      <div class="text-[10px] text-zinc-500 uppercase">Counter Hit</div>
      <div class="text-sm font-bold text-purple-400">Launch</div>
    </div>
    <div class="bg-[#0B0C12] p-2 rounded border border-zinc-800/60">
      <div class="text-[10px] text-zinc-500 uppercase">Damage</div>
      <div class="text-sm font-bold text-amber-400">23 dmg</div>
    </div>
  </div>
</div>
```

---

### 4. Tekken 8 Slanted Action Button (Aggressive Cyber Button)
Tekken 8 ke buttons mein `clip-path` (kate hue kinaray) ya `-skew-x-12` use hota hai jiske peeche neon glow hota hai.

```html
<!-- Tekken 8 Primary Slanted CTA Button -->
<button class="group relative inline-flex items-center justify-center px-8 py-3 font-black uppercase italic tracking-widest text-white bg-gradient-to-r from-[#FF0055] to-[#D90429] transform -skew-x-12 hover:from-[#00F0FF] hover:to-[#0077FF] hover:text-black transition-all duration-300 shadow-[0_0_20px_rgba(255,0,85,0.5)] hover:shadow-[0_0_30px_rgba(0,240,255,0.8)] active:scale-95">
  <!-- Top-left corner cut accent -->
  <span class="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-white"></span>
  <!-- Button Text (Un-skewed slightly for readability) -->
  <span class="transform skew-x-12 flex items-center gap-2">
    VIEW FRAME DATA <span>⚡</span>
  </span>
</button>
```

---

## PART 2: WORLD-FAMOUS WEBSITES UI BREAKDOWN (BUTTONS, CARDS & IMAGES)

Agar aap apni website mein Tekken 8 ke aggressive gaming look ko duniya ki top tech websites ki smoothness ke sath mix karna chahte hain, toh yeh 5 world-famous styles best hain:

### 1. Linear.app & Vercel Style: "Spotlight Border Glow Card"
Duniya mein aaj kal dark-mode websites par **Linear.app** aur **Vercel** ka card style #1 par hai. Ismein card ka border bahut baarik (`1px`) hota hai aur upar se halki si roshni (top radial gradient glow) pad rahi hoti hai.

```html
<!-- Linear / Vercel Spotlight Card -->
<div class="relative rounded-2xl bg-zinc-950 p-[1px] overflow-hidden group">
  <!-- Glowing Top Border Line -->
  <div class="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/50 to-transparent"></div>
  
  <!-- Inner Card Body -->
  <div class="relative h-full bg-gradient-to-b from-zinc-900/90 to-zinc-950 rounded-2xl p-6 border border-white/10 group-hover:border-white/20 transition-colors">
    <div class="w-10 h-10 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center mb-4 text-white">
      ✦
    </div>
    <h3 class="text-lg font-semibold text-white tracking-tight">Ultra-Fast Frame Lookup</h3>
    <p class="text-sm text-zinc-400 mt-2 leading-relaxed">
      Instant filter by startup frames (`i10`–`i15`), homing moves, and wall-splat punishers with zero page reload.
    </p>
  </div>
</div>
```

---

### 2. Apple.com Style: "Bento Grid & Frosted Glass Image Display"
Apple apni websites par **Bento Grid** (chote-bade asymmetric boxes) aur **Frosted Glass (`backdrop-blur-xl`)** use karta hai. Image display hamesha rounded corners (`rounded-3xl`) aur smooth zoom-on-hover ke sath hota hai.

```html
<!-- Apple Bento Card with Glass Overlay -->
<div class="relative w-full h-72 rounded-3xl overflow-hidden bg-zinc-900 border border-white/10 group">
  <!-- Background High-Res Image / GIF Preview -->
  <img src="https://placehold.co/800x500/090A0F/00F0FF?text=Move+Hitbox+GIF+Preview" 
       alt="Hitbox Preview" 
       class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out" />
  
  <!-- Apple Frosted Glass Floating Pill Bar at Bottom -->
  <div class="absolute bottom-4 inset-x-4 p-4 rounded-2xl bg-black/50 backdrop-blur-xl border border-white/15 flex items-center justify-between">
    <div>
      <p class="text-xs font-medium text-zinc-300">60 FPS Frame-by-Frame</p>
      <h4 class="text-sm font-bold text-white">Slow-Motion Hitbox Visualizer</h4>
    </div>
    <button class="px-4 py-2 rounded-full bg-white text-black text-xs font-bold hover:bg-zinc-200 transition">
      Play GIF
    </button>
  </div>
</div>
```

---

### 3. Stripe.com Style: "Animated Pill Button with Sliding Arrow"
Stripe ke buttons mein ek chota arrow (`→`) hota hai jo normal state mein simple dikhta hai, lekin hover karne par uske peeche ek line ban jati hai aur arrow aage slide karta hai.

```html
<!-- Stripe Famous Animated Arrow Button -->
<button class="group inline-flex items-center gap-2 px-6 py-3 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-[0_10px_20px_-10px_rgba(79,70,229,0.6)] transition-all duration-200">
  <span>Explore All Characters</span>
  <span class="transform group-hover:translate-x-1 transition-transform duration-200">→</span>
</button>
```

---

### 4. Riot Games (Valorant) Style: "Outlined Technical Corner-Cut Card"
Valorant aur Tekken 8 dono mein **HUD / Sci-Fi Tactical UI** use hota hai. Ismein card ke kinaray par chote `+` निशान (crosshairs) aur technical serial numbers (`// 01`) likhe hote hain.

```html
<!-- Valorant / Tactical Gaming Image & Info Card -->
<div class="relative bg-[#0F1923] border border-zinc-700 p-5 text-white">
  <!-- Corner Crosshair Accents -->
  <span class="absolute -top-1 -left-1 w-2 h-2 bg-[#FF4655]"></span>
  <span class="absolute -bottom-1 -right-1 w-2 h-2 bg-[#FF4655]"></span>
  
  <div class="flex justify-between items-center text-[10px] font-mono text-zinc-400 mb-3">
    <span>// SYS.COMBO_DATA</span>
    <span>DMG: 84 (WALL CARRY)</span>
  </div>

  <!-- Combo Sequence Box -->
  <div class="bg-black/60 p-3 border-l-4 border-[#FF4655] font-mono text-sm text-zinc-200">
    df+2 ➔ f+4 ➔ df+1,4 (Tornado) ➔ dash ➔ b+3~f, 1, 2
  </div>
</div>
```

---

## PART 3: READY-TO-USE AI PROMPTS TO BUILD YOUR WEBSITE

Agar aap chahte hain ke main (ya koi bhi AI) aapke liye poori **Tekken 8 Move-List + Modern UI Website** code kar de, toh aap ye prompts copy-paste kar sakte hain:

### Prompt 1: Complete Tekken 8 Move-List & Frame Data Website
> *"Build a complete, responsive single-file HTML/Tailwind CSS web application for a Tekken 8 Move List & Frame Data Hub (inspired by Wavu Wiki, TekkenDocs, and the official Bandai Namco Tekken 8 UI). Include: (1) A slanted `-skew-x-6` Character Select Roster grid with hover glow effects, (2) An interactive Search & Filter bar (filter by Heat Engagers, Launchers, Homing, i10-i15 Punishers, and Safe on Block moves), (3) Move Cards with visual input buttons (directional arrows + color-coded 1, 2, 3, 4 attack buttons) and color-coded Frame Data badges (Startup, On Block, On Hit, Counter Hit), and (4) An Apple/Linear style dark glassmorphic modal for viewing slow-motion move previews and combo guides."*

### Prompt 2: Mixing Apple Bento Grid with Gaming UI
> *"Create a Hero Section and Feature Bento Grid combining Linear.app's dark spotlight borders, Apple's frosted glass (`backdrop-blur-xl`), and Tekken 8's neon crimson/cyan aggressive typography. Include animated hover cards, a live frame-punish calculator widget, and slanted CTA buttons."*