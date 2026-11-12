"""Redrawn taxonomy chart: the eight Figure 4B categories by feature count."""

rows = [
    ("잔기 정체", 88),
    ("2차 구조", 1895),
    ("3차 모티프", 1554),
    ("도메인 / 폴드", 2546),
    ("무질서 / 저복잡도", 686),
    ("생화학적 환경", 1770),
    ("국재화 / 토폴로지", 2319),
    ("기능 부위 / 영역", 5382),
]
total = sum(v for _, v in rows)
codebook = 16384

W, H = 760, 420
L, R, T = 150, 78, 56          # label gutter, right gutter, top
bar_h, gap = 26, 14
x0, x1 = L, W - R
vmax = 6000
sx = lambda v: (x1 - x0) * v / vmax

ticks = [0, 2000, 4000, 6000]

p = []
p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="SAE 특징 8개 범주별 개수">')
p.append("""<style>
  .srf{fill:#fffff8}
  .ttl{font:600 16px/1.3 ui-sans-serif,system-ui,sans-serif;fill:#1a1a16}
  .sub{font:12.5px ui-sans-serif,system-ui,sans-serif;fill:#6b6b63}
  .cat{font:13px ui-sans-serif,system-ui,sans-serif;fill:#2a2a24}
  .val{font:600 12.5px ui-sans-serif,system-ui,sans-serif;fill:#3a3a32}
  .tick{font:11px ui-sans-serif,system-ui,sans-serif;fill:#8a8a80}
  .grid{stroke:#d9d9cd;stroke-width:1}
  .axis{stroke:#b6b6a8;stroke-width:1}
  .bar{fill:#0b7471}
  .bar--hi{fill:#b9760c}
  @media (prefers-color-scheme: dark){
    .srf{fill:#15151a}
    .ttl{fill:#ecece4}.sub{fill:#9a9a90}.cat{fill:#d8d8d0}.val{fill:#c8c8be}
    .tick{fill:#8a8a80}.grid{stroke:#33333c}.axis{stroke:#4a4a52}
    .bar{fill:#4fb8b4}.bar--hi{fill:#e3a443}
  }
</style>""")
p.append(f'<rect class="srf" width="{W}" height="{H}"/>')
p.append(f'<text class="ttl" x="16" y="26">16,384개 특징을 8개 범주로 나누면</text>')
p.append(f'<text class="sub" x="16" y="44">ESMC 6B 60층 SAE · 분류된 합계 {total:,}개 (사전의 {total/codebook*100:.1f}%)</text>')

for t in ticks:
    x = x0 + sx(t)
    p.append(f'<line class="grid" x1="{x:.1f}" y1="{T-6}" x2="{x:.1f}" y2="{T + len(rows)*(bar_h+gap) - gap + 6:.1f}"/>')
    p.append(f'<text class="tick" x="{x:.1f}" y="{T + len(rows)*(bar_h+gap) + 14:.0f}" text-anchor="middle">{t:,}</text>')

for i, (name, v) in enumerate(rows):
    y = T + i * (bar_h + gap)
    w = max(sx(v), 2)
    cls = "bar bar--hi" if v == max(r[1] for r in rows) else "bar"
    p.append(f'<text class="cat" x="{L-14}" y="{y + bar_h*0.72:.1f}" text-anchor="end">{name}</text>')
    p.append(f'<rect class="{cls}" x="{x0}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="4">'
             f'<title>{name}: {v:,}개</title></rect>')
    p.append(f'<text class="val" x="{x0 + w + 9:.1f}" y="{y + bar_h*0.72:.1f}">{v:,}</text>')

p.append(f'<line class="axis" x1="{x0}" y1="{T-6}" x2="{x0}" y2="{T + len(rows)*(bar_h+gap) - gap + 6:.1f}"/>')
p.append('</svg>')

out = "/home/claude/eden-repo/content/posts/2026-11-12-esmc-sae/imgs/taxonomy.svg"
open(out, "w").write("\n".join(p))
print(out, "total", total, "of", codebook)
