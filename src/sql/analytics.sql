-- KPIs gerais
SELECT
    COUNT(*) AS total_chamados,
    SUM(is_resolved) AS chamados_resolvidos,
    ROUND(100.0 * SUM(is_resolved) / COUNT(*), 1) AS taxa_resolucao_pct,
    ROUND(AVG(CASE WHEN is_resolved = 1 THEN resolution_hours END), 1) AS tempo_medio_horas,
    ROUND(100.0 * AVG(CASE WHEN is_resolved = 1 THEN sla_met END), 1) AS sla_cumprido_pct,
    ROUND(AVG(satisfaction), 2) AS satisfacao_media
FROM tickets;

-- Categorias com maior demanda e desempenho
SELECT
    category,
    COUNT(*) AS total_chamados,
    ROUND(AVG(CASE WHEN is_resolved = 1 THEN resolution_hours END), 1) AS tempo_medio_horas,
    ROUND(100.0 * AVG(CASE WHEN is_resolved = 1 THEN sla_met END), 1) AS sla_cumprido_pct
FROM tickets
GROUP BY category
ORDER BY total_chamados DESC;

-- Evolucao mensal
SELECT
    year_month,
    COUNT(*) AS total_chamados,
    SUM(CASE WHEN is_resolved = 0 THEN 1 ELSE 0 END) AS em_aberto,
    ROUND(100.0 * AVG(CASE WHEN is_resolved = 1 THEN sla_met END), 1) AS sla_cumprido_pct
FROM tickets
GROUP BY year_month
ORDER BY year_month;

-- Itens em aberto priorizados
SELECT ticket_id, created_at, category, priority, channel, location
FROM tickets
WHERE is_resolved = 0
ORDER BY
    CASE priority
        WHEN 'Crítica' THEN 1
        WHEN 'Alta' THEN 2
        WHEN 'Média' THEN 3
        ELSE 4
    END,
    created_at;
