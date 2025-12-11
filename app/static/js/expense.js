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
// console.log(categoryNames);
// console.log(categoryTotals);

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

// Function to show toast
function showToast(title, message) {
    document.getElementById('toastTitle').innerText = title;
    document.getElementById('toastBody').innerText = message;
    $('#messageToast').toast('show');
}

// Example usage:
// showToast('Success', 'Category added successfully!');
$(document).ready(function () {
    $("#addCategoryForm").submit(function (e) {
        e.preventDefault();   // Stop normal form submit

        let categoryName = $("#categoryName").val();

        $.ajax({
            url: ADD_CATEGORY_URL,
            method: "POST",
            data: {
                category: categoryName,
                csrfmiddlewaretoken: CSRF_TOKEN
            },
            success: function (response) {

                if (response.status === "success") {

                    // Close modal
                    $("#addCategoryModal").modal("hide");

                    // Clear input
                    $("#categoryName").val("");

                    // Show toast
                    showToast("Success", response.message);

                    // Inject new category into dropdown immediately
                    $("select[name='category']").append(
                        `<option value="${response.id}" class="text-capitalize">${response.name}</option>`
                    );

                    // Update chart data
                    updateCharts(response.chartNames, response.chartTotals);
                } 
                else {
                    showToast("Error", response.message);
                }
            },
            error: function () {
                showToast("Error", "Something went wrong!");
            }
        });
    });
});


// ------------------------------------------------------
// 🔥 Function to update charts dynamically without reload
// ------------------------------------------------------
function updateCharts(names, totals) {

    // Update pie chart
    expenseChart.data.labels = names;
    expenseChart.data.datasets[0].data = totals;
    expenseChart.update();
}
