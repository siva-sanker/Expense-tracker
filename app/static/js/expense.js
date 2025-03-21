const categoryNames = JSON.parse(document.getElementById('categoryNames').textContent);
const categoryTotals = JSON.parse(document.getElementById('categoryTotals').textContent);

const ctx = document.getElementById('expenseChart').getContext('2d');
const expenseChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: categoryNames, // Use the parsed category names
        datasets: [{
            data: categoryTotals, // Use the parsed totals
            backgroundColor: [
                '#FF6384', '#36A2EB', '#FFCE56', '#4CAF50', '#FFC107','orange'
            ],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom', // Set legend to bottom
            }
        }
    }
});
console.log(categoryNames);
console.log(categoryTotals);

const lineChartData = JSON.parse(document.getElementById('lineChartData').textContent);

const labels = lineChartData.map(dataPoint => dataPoint.label);
const values = lineChartData.map(dataPoint => dataPoint.value);

const cty = document.getElementById('lineChart').getContext('2d');
const lineChart = new Chart(cty, {
    type: 'line', // Set chart type to 'line'
    data: {
        labels: labels, // Labels: ['Salary', 'Expenses', 'Remaining']
        datasets: [{
            label: 'Balance Overview',
            data: values, // Data: [Salary, Total Expense, Remaining Balance]
            borderColor: '#36A2EB', // Line color
            backgroundColor: 'rgba(54, 162, 235, 0.2)', // Fill under the line
            borderWidth: 2,
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Metrics'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Amount (INR)'
                },
                beginAtZero: true
            }
        }
    }
});
