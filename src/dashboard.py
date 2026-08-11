"""Gera um dashboard HTML portatil, sem servidor e sem bibliotecas JavaScript."""

from __future__ import annotations

import html
import json
from pathlib import Path

import pandas as pd


def _records_for_browser(data: pd.DataFrame) -> list[dict[str, object]]:
    fields = [
        "ticket_id",
        "created_date",
        "category",
        "priority",
        "channel",
        "location",
        "status",
        "resolution_hours",
        "sla_met",
        "satisfaction",
    ]
    records = data[fields].copy().astype(object)
    records = records.where(pd.notna(records), None)
    return records.to_dict(orient="records")


def generate_dashboard(data: pd.DataFrame, output_path: Path) -> Path:
    """Escreve uma pagina interativa com filtros e KPIs calculados no navegador."""
    records_json = json.dumps(_records_for_browser(data), ensure_ascii=False)
    title = html.escape("Painel de Chamados de TI")
    template = r'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Dashboard de indicadores de suporte de TI com dados sintéticos.">
  <title>__TITLE__</title>
  <style>
    :root { --navy:#102a43; --blue:#2878bd; --cyan:#39a0ca; --ink:#243b53; --muted:#627d98; --line:#d9e2ec; --bg:#f4f7fa; --good:#2f855a; --warn:#c05621; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:Inter,Segoe UI,Arial,sans-serif; color:var(--ink); background:var(--bg); }
    header { background:linear-gradient(120deg,var(--navy),#1d4e73); color:white; padding:36px max(24px,calc((100vw - 1180px)/2)); }
    header p { margin:7px 0 0; color:#d9eaf7; }
    main { max-width:1180px; margin:0 auto; padding:26px 24px 44px; }
    .filters,.cards,.grid { display:grid; gap:16px; }
    .filters { grid-template-columns:repeat(3,minmax(0,1fr)); background:white; padding:16px; border:1px solid var(--line); border-radius:14px; }
    label { color:var(--muted); font-size:.82rem; font-weight:700; }
    select { width:100%; margin-top:6px; padding:10px 12px; border:1px solid var(--line); border-radius:9px; background:white; color:var(--ink); }
    .cards { grid-template-columns:repeat(5,minmax(0,1fr)); margin:18px 0; }
    .card,.panel { background:white; border:1px solid var(--line); border-radius:14px; box-shadow:0 4px 18px rgba(36,59,83,.05); }
    .card { padding:18px; }
    .card span { color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.04em; font-weight:700; }
    .card strong { display:block; margin-top:7px; color:var(--navy); font-size:1.75rem; }
    .grid { grid-template-columns:1fr 1fr; }
    .panel { padding:20px; }
    h1 { margin:0; font-size:2rem; }
    h2 { margin:0 0 18px; font-size:1.05rem; color:var(--navy); }
    .bar-row { display:grid; grid-template-columns:150px 1fr 48px; align-items:center; gap:10px; margin:12px 0; font-size:.85rem; }
    .bar-track { height:11px; background:#eaf0f5; border-radius:999px; overflow:hidden; }
    .bar { height:100%; background:linear-gradient(90deg,var(--blue),var(--cyan)); border-radius:999px; }
    table { width:100%; border-collapse:collapse; font-size:.82rem; }
    th,td { padding:10px 8px; border-bottom:1px solid var(--line); text-align:left; }
    th { color:var(--muted); font-size:.73rem; text-transform:uppercase; }
    .wide { grid-column:1/-1; overflow:auto; }
    .badge { display:inline-block; padding:4px 8px; border-radius:999px; background:#eaf4ff; color:#1d5f91; font-weight:700; font-size:.72rem; }
    footer { text-align:center; color:var(--muted); padding:8px 24px 30px; font-size:.78rem; }
    @media (max-width:900px) { .cards{grid-template-columns:repeat(2,1fr)} .grid{grid-template-columns:1fr} .filters{grid-template-columns:1fr} }
  </style>
</head>
<body>
<header><h1>__TITLE__</h1><p>Indicadores de volume, resolução, SLA e satisfação - dados 100% sintéticos.</p></header>
<main>
  <section class="filters" aria-label="Filtros">
    <label>Prioridade<select id="priority"><option value="">Todas</option></select></label>
    <label>Categoria<select id="category"><option value="">Todas</option></select></label>
    <label>Local<select id="location"><option value="">Todos</option></select></label>
  </section>
  <section class="cards">
    <article class="card"><span>Chamados</span><strong id="total">0</strong></article>
    <article class="card"><span>Resolvidos</span><strong id="resolved">0%</strong></article>
    <article class="card"><span>SLA cumprido</span><strong id="sla">0%</strong></article>
    <article class="card"><span>Tempo médio</span><strong id="hours">0h</strong></article>
    <article class="card"><span>Satisfação</span><strong id="sat">0/5</strong></article>
  </section>
  <section class="grid">
    <article class="panel"><h2>Volume por categoria</h2><div id="category-bars"></div></article>
    <article class="panel"><h2>Volume por prioridade</h2><div id="priority-bars"></div></article>
    <article class="panel wide"><h2>Ultimos chamados no recorte</h2><table><thead><tr><th>ID</th><th>Data</th><th>Categoria</th><th>Prioridade</th><th>Status</th><th>Tempo</th></tr></thead><tbody id="tickets"></tbody></table></article>
  </section>
</main>
<footer>Projeto de portfólio - Python, pandas, SQL, ETL e JavaScript.</footer>
<script>
const tickets = __DATA__;
const $ = id => document.getElementById(id);
const unique = key => [...new Set(tickets.map(t => t[key]))].sort();
for (const [id,key] of [['priority','priority'],['category','category'],['location','location']]) {
  unique(key).forEach(value => { const option=document.createElement('option'); option.value=value; option.textContent=value; $(id).appendChild(option); });
  $(id).addEventListener('change', render);
}
const pct = (part,total) => total ? (part/total*100) : 0;
function bars(containerId, data, labelKey) {
  const target=$(containerId); target.innerHTML=''; const max=Math.max(...data.map(d=>d.total),1);
  data.forEach(d=>{ target.insertAdjacentHTML('beforeend', `<div class="bar-row"><span>${d[labelKey]}</span><div class="bar-track"><div class="bar" style="width:${d.total/max*100}%"></div></div><strong>${d.total}</strong></div>`); });
}
function group(rows,key){ const map={}; rows.forEach(r=>map[r[key]]=(map[r[key]]||0)+1); return Object.entries(map).map(([label,total])=>({[key]:label,total})).sort((a,b)=>b.total-a.total); }
function render(){
  const filtered=tickets.filter(t=>(!$('priority').value||t.priority===$('priority').value)&&(!$('category').value||t.category===$('category').value)&&(!$('location').value||t.location===$('location').value));
  const resolved=filtered.filter(t=>t.resolution_hours!==null); const sla=resolved.filter(t=>t.sla_met===true); const sats=resolved.map(t=>t.satisfaction).filter(v=>v!==null); const hours=resolved.map(t=>t.resolution_hours);
  $('total').textContent=filtered.length.toLocaleString('pt-BR'); $('resolved').textContent=pct(resolved.length,filtered.length).toFixed(1).replace('.',',')+'%'; $('sla').textContent=pct(sla.length,resolved.length).toFixed(1).replace('.',',')+'%'; $('hours').textContent=(hours.reduce((a,b)=>a+b,0)/(hours.length||1)).toFixed(1).replace('.',',')+'h'; $('sat').textContent=(sats.reduce((a,b)=>a+b,0)/(sats.length||1)).toFixed(2).replace('.',',')+'/5';
  bars('category-bars',group(filtered,'category'),'category'); bars('priority-bars',group(filtered,'priority'),'priority');
  $('tickets').innerHTML=filtered.slice().sort((a,b)=>b.created_date.localeCompare(a.created_date)||b.ticket_id-a.ticket_id).slice(0,10).map(t=>`<tr><td>#${t.ticket_id}</td><td>${t.created_date}</td><td>${t.category}</td><td><span class="badge">${t.priority}</span></td><td>${t.status}</td><td>${t.resolution_hours===null?'Em aberto':t.resolution_hours.toFixed(1).replace('.',',')+'h'}</td></tr>`).join('');
}
render();
</script>
</body></html>'''
    page = template.replace("__TITLE__", title).replace("__DATA__", records_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(page, encoding="utf-8")
    return output_path
