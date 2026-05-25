(function () {
    'use strict';

    const BRAND_COLORS = [
        '#C21631',
        '#132041',
        '#4F6A84',
        '#A0B3C6',
        '#DB5472',
        '#25405B',
        '#6B8CA8',
        '#030E2A',
    ];

    const chartFont = {
        family: "'Proxima Nova', Arial, sans-serif",
        size: 12,
    };

    function readJson(id) {
        const el = document.getElementById(id);
        if (!el) return [];
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            return [];
        }
    }

    function truncateLabel(text, maxLen) {
        if (!text) return '—';
        return text.length > maxLen ? text.slice(0, maxLen) + '…' : text;
    }

    function initProductsChart(products) {
        const canvas = document.getElementById('productsChart');
        if (!canvas || typeof Chart === 'undefined') return;

        const labels = products.map((p) => truncateLabel(p.name, 22));
        const data = products.map((p) => p.quantity);

        new Chart(canvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Количество',
                    data: data,
                    backgroundColor: BRAND_COLORS[0],
                    borderRadius: 6,
                    maxBarThickness: 48,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    x: {
                        ticks: { color: '#4F6A84', font: chartFont, maxRotation: 45 },
                        grid: { display: false },
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#4F6A84', font: chartFont, stepSize: 1 },
                        grid: { color: '#EDF6FF' },
                    },
                },
            },
        });
    }

    function initCategoriesChart(categories) {
        const canvas = document.getElementById('categoriesChart');
        if (!canvas || typeof Chart === 'undefined') return;

        const labels = categories.map((c) => c.name);
        const data = categories.map((c) => c.quantity);

        new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: BRAND_COLORS,
                    borderWidth: 2,
                    borderColor: '#ffffff',
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#132041', font: chartFont, padding: 14 },
                    },
                },
            },
        });
    }

    let timelineChart = null;

    function initTimelineChart(timeline) {
        const canvas = document.getElementById('timelineChart');
        if (!canvas || typeof Chart === 'undefined') return;

        const labels = timeline.map((t) => t.date);
        const orders = timeline.map((t) => t.orders);
        const revenue = timeline.map((t) => t.revenue);

        if (timelineChart) {
            timelineChart.destroy();
        }

        timelineChart = new Chart(canvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Заказы',
                        data: orders,
                        borderColor: '#132041',
                        backgroundColor: 'rgba(19, 32, 65, 0.08)',
                        fill: true,
                        tension: 0.35,
                        yAxisID: 'y',
                    },
                    {
                        label: 'Выручка, ₽',
                        data: revenue,
                        borderColor: '#C21631',
                        backgroundColor: 'rgba(194, 22, 49, 0.06)',
                        fill: false,
                        tension: 0.35,
                        yAxisID: 'y1',
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: {
                        labels: { color: '#132041', font: chartFont },
                    },
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#4F6A84',
                            font: chartFont,
                            autoSkip: false,
                            maxRotation: 45,
                            minRotation: 0,
                        },
                        grid: { color: '#EDF6FF' },
                    },
                    y: {
                        type: 'linear',
                        position: 'left',
                        beginAtZero: true,
                        ticks: { color: '#4F6A84', font: chartFont, stepSize: 1 },
                        grid: { color: '#EDF6FF' },
                    },
                    y1: {
                        type: 'linear',
                        position: 'right',
                        beginAtZero: true,
                        ticks: { color: '#C21631', font: chartFont },
                        grid: { drawOnChartArea: false },
                    },
                },
            },
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        const products = readJson('top-products-data');
        const categories = readJson('top-categories-data');
        const timeline = readJson('orders-timeline-data');

        initProductsChart(products);
        initCategoriesChart(categories);
        initTimelineChart(timeline);
    });
})();
