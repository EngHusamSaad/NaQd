src="https://cdn.jsdelivr.net/npm/chart.js"
src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"
const csrfToken = '{{ csrf_token }}'


//View_customer_by_Fetch
document.addEventListener("DOMContentLoaded", function () {
document.getElementById("customers-link").addEventListener("click", function () {
    fetch("/api/customers/")
      .then((response) => response.json())
      .then((data) => {
        let content = '<table class="table table-striped">';
        content +=
          "<thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Mobile</th><th>Actions</th></tr></thead><tbody>";
        add_button =
          ' <a href="/register" class="btn btn-primary btn-lg active" role="button" aria-pressed="true">Add Customer</a>';
        let counter = `<strong>Total Customers: ${data.count}</strong>`;

        data.customers.forEach((customer, index) => {
          content += `<tr>
                                    <td>${index + 1}</td>
                                    <td>${customer.first_name} ${customer.second_name}</td>
                                    <td>${customer.email}</td>
                                    <td>${customer.mobile}</td>
                                <td>
                    <div class="actions">
                        <!-- زر التعديل -->
                        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editCustomerModal" data-id="${customer.id
            }">
                            Edit
                        </button>
                        <!-- زر الحذف -->
                        <button type="button" class="btn btn-danger" onclick="deleteCustomer(${customer.id
            })">
                            Delete
                        </button>
                    </div>
                </td>
            </tr>`;
        });
        content += "</tbody></table>";
        document.getElementById("content").innerHTML =
          add_button + content + counter;
        document.getElementById("head_title").textContent = "Customer";
      });
  });
});

document.addEventListener("DOMContentLoaded", function () {
document
  .getElementById("debts-link")
  .addEventListener("click", function () {
    loaddebtspage();
  });
});

// View_Debts_by_Fetch
function loaddebtspage() {
  // تحميل الديون بشكل أولي
  fetch("/api/debts/")
    .then((response) => response.json())
    .then((data) => {
      let content = '<table class="table table-striped">';
      content += "<thead><tr><th>ID</th><th>Amount</th><th>Status</th><th>Customer</th><th>Actions</th></tr></thead><tbody>";

      let nav_block =
        '<nav class="navbar navbar-light bg-light">' +
        '<form class="form-inline" id="searchForm">' +
        '<input class="form-control mr-sm-2" type="search" id="searchInput" placeholder="Search" aria-label="Search">' +
        '<button class="btn btn-outline-success my-2 my-sm-0" type="submit" id="searchButton">Search</button>' +
        '</form>' +
        '<button type="button" class="btn btn-primary btn-lg active" data-bs-toggle="modal" data-bs-target="#customerModal">Add Debts</button>' +
        '</nav>';

      // إضافة الديون في الجدول
      data.forEach((debt, index) => {
        content += `<tr>
                        <td>${index + 1}</td>
                        <td>${debt.amount_debt}</td>
                        <td>
                            <span style="padding: 5px 10px; border-radius: 5px; color: white;"
                                  class="${debt.status_debt ? "bg-success" : "bg-danger"}">
                              ${debt.status_debt ? "Paid" : "Unpaid"}
                            </span>
                        </td>
                        <td><strong>${debt.customer_name}</strong></td>
                        <td>
                          <div class="actions">
                           <button type="button" class="btn btn-primary" onclick="openEditModal(${debt.id}, '${debt.amount_debt}', '${debt.notes}')" data-bs-toggle="modal"
                              data-bs-target="#exampleModal" data-id="${debt.id}">
                              Edit
                          </button>
                            <button type="button" class="btn btn-warning send-reminder" data-id="${debt.id}">Send Reminder</button>
                            <button type="button" class="btn btn-danger delete-btn" data-id="${debt.id}">
                                Delete
                            </button>
                          </div>
                        </td>
                    </tr>`;
      });

      content += "</tbody></table>";
      document.getElementById("content").innerHTML = nav_block + content;
      document.getElementById("head_title").textContent = "Debts";

      // البحث
      document.getElementById("searchForm").addEventListener("submit", function (event) {
        event.preventDefault(); // منع إرسال النموذج

        let query = document.getElementById("searchInput").value.toLowerCase(); // الحصول على الكلمة المدخلة
        if (query === "") {
          // إذا كان حقل البحث فارغًا، قم بتحميل الديون مجددًا
          loaddebtspage();
        } else {
          // إرسال طلب بحث للـ API مع الكلمة المدخلة
          fetch(`/api/debts/?search=${query}`)
            .then((response) => response.json())
            .then((data) => {
              let searchContent = '<table class="table table-striped">';
              searchContent += "<thead><tr><th>ID</th><th>Amount</th><th>Status</th><th>Customer</th><th>Actions</th></tr></thead><tbody>";

              // عرض الديون المصفاة بناءً على البحث
              data.forEach((debt, index) => {
                searchContent += `<tr>
                            <td>${index + 1}</td>
                            <td>${debt.amount_debt}</td>
                            <td>
                                <span style="padding: 5px 10px; border-radius: 5px; color: white;"
                                      class="${debt.status_debt ? "bg-success" : "bg-danger"}">
                                  ${debt.status_debt ? "Paid" : "Unpaid"}
                                </span>
                            </td>
                            <td><strong>${debt.customer_name}</strong></td>
                            <td>
                              <div class="actions">
                                <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                    data-bs-target="#exampleModal" data-id="${debt.id}">
                                    Edit
                                </button>
                                <button type="button" class="btn btn-warning send-reminder" data-id="${debt.id}">
                                    Send Reminder
                                </button>
                                <form action="delete_item" method="post">
                                  {% csrf_token %}
                                  <input type="hidden" name="item_id" value="${debt.id}">
                                  <button type="submit" class="btn btn-danger">Delete</button>
                                </form>
                              </div>
                            </td>
                        </tr>`;
              });

              searchContent += "</tbody></table>";
              document.getElementById("content").innerHTML = nav_block + searchContent;
            });
        }
      });
 

      // إضافة الحدث إلى زر "Send Reminder"
      document.querySelectorAll(".send-reminder").forEach((button) => {
        button.addEventListener("click", function () {
          const debtId = this.getAttribute("data-id");

          // إرسال الطلب عبر Fetch
          fetch("/send_reminder/", {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
              "X-CSRFToken": getCookie("csrftoken"), // للحصول على CSRF
            },
            body: `debt_id=${debtId}`,
          })
            .then((response) => response.json())
            .then((result) => {
              const alertBox = document.createElement("div");
              alertBox.className = `alert ${result.message.includes("successfully") ? "alert-success" : "alert-danger"} fade show`;
              alertBox.textContent = result.message;
              alertBox.style.position = "fixed";
              alertBox.style.top = "10px";
              alertBox.style.right = "10px";
              alertBox.style.zIndex = "1050";
              alertBox.style.padding = "15px";
              alertBox.style.borderRadius = "5px";

              document.body.appendChild(alertBox);

              // إخفاء الإشعار بعد 3 ثوانٍ
              setTimeout(() => alertBox.remove(), 3000);
            })
            .catch((error) => {
              alert("An error occurred: " + error);
            });
        });
      });
    });
}


// دالة للحصول على CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;
}

//View_Payments_by_Fetch
document.addEventListener("DOMContentLoaded", function () {
document
  .getElementById("payments-link")
  .addEventListener("click", function () {
    fetch("/api/payments/")
      .then((response) => response.json())
      .then((data) => {
        let content = '<table class="table table-striped">';
        content +=
          "<thead><tr><th>ID</th><th>Payment Type</th><th>Payment Amount</th><th>Customer Name</th><th>Created At</th><th>Total Debt Amount</th><th>Remaining Debt</th><th>Actions</th></tr></thead><tbody>";

        add_button =
          '<button type="button" class="btn btn-primary btn-lg active" data-bs-toggle="modal" data-bs-target="#paymentModal" data-id="${payment.id}"> Add Payment </button>';

        data.forEach((payment, index) => {
          content += `
                            <tr>
                                <td>${index + 1}</td>
                                <td>${payment.payment_type}</td>
                                <td>${payment.amount_payment}</td>
                                <td>${payment.customer_name}</td>
                                <td>${payment.created_at}</td>
                                <td>${payment.total_debt}</td>
                                <td>${payment.amount_remain}</td>
                                <td>
                                    <div class="actions">
                                        <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                            data-bs-target="#editPaymentModal" data-id="${payment.id
            }">
                                            Edit
                                        </button>
                                        <form action="delete_item" method="post">
                                            {% csrf_token %}
                                            <input type="hidden" name="item_id" value="${payment.id
            }">
                                            <button type="submit" class="btn btn-danger">Delete</button>
                                        </form>
                                    </div>
                                </td>

                            </tr>`;
        });
        content += "</tbody></table>";
        document.getElementById("content").innerHTML =
          add_button + content; // إضافة الزر بعد تحميل الجدول
        document.getElementById("head_title").textContent = "Payments";
      });
  });
});

//View_Dashboard_by_Fetch
document.addEventListener("DOMContentLoaded", function () {
  // تنفيذ الكود تلقائيًا عند تحميل الصفحة
  loadDashboard();

  // ربط الزر ليعرض الـ Dashboard عند النقر عليه
  document
    .getElementById("dashboard_page")
    .addEventListener("click", function () {
      loadDashboard();
    });
});

function loadDashboard() {
  const content = document.getElementById("content");
  if (!content) {
    alert("المحتوى غير موجود!");
    return;
  }
  content.innerHTML = "";
  const gridContainer = document.createElement("div");
  gridContainer.id = "grid-container";
  content.appendChild(gridContainer);

  for (let i = 1; i <= 2; i++) {
    const chartContainer = document.createElement("div");
    chartContainer.className = "chart-box";
    const chartCanvas = document.createElement("canvas");
    chartCanvas.id = `chart${i}`;
    chartContainer.appendChild(chartCanvas);
    gridContainer.appendChild(chartContainer);
    document.getElementById("head_title").textContent = "Dashboard";
    chart_label = ["Debts Chart", "Payment Chart"];

    fetch(`/chart-data-${i}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("فشل في جلب البيانات من الخادم!");
        }
        return response.json();
      })
      .then((data) => {
        const ctx = chartCanvas.getContext("2d");
        window[`myChart${i}`] = new Chart(ctx, {
          type: i % 2 === 0 ? "doughnut" : "bar", // تبديل النوع بين خطي وعمودي
          data: {
            labels: data.labels,
            datasets: [
              {
                label: chart_label[i - 1],
                data: data.values,
                backgroundColor: ["red", "blue", "green", "yellow"],
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false, // السماح بتعديل الحجم
            aspectRatio: i === 2 ? 1 : 2, // تصغير الحجم للرسم البياني الثاني
            plugins: {
              title: {
                display: i === 2,
                text: i === 1 ? "Debts Chart" : "Payment Chart",
                font: {
                  size: 18,
                  weight: "bold",
                },
                padding: {
                  top: 20,
                },
              },
            },
          },
        });
      })
      .catch((error) => {
        console.error("خطأ:", error);
        alert(`حدث خطأ أثناء تحميل بيانات الرسم البياني ${i}!`);
      });
  }
  const tableContainer = document.createElement("div");
  tableContainer.className = "table-responsive mt-4 chart-box";

  const tableTitle = document.createElement("h4");
  tableTitle.className = "mb-3";
  tableTitle.textContent = "Latest Customers";
  tableTitle.style.textAlign = "center";

  tableTitle.style.padding = "10px";

  tableContainer.appendChild(tableTitle);

  const table = document.createElement("table");
  table.className = "table table-striped table-bordered "; // تنسيق الجدول باستخدام فئات Bootstrap
  table.innerHTML = `
          <thead class="thead-dark">
            <tr><strong>
              <th><strong>Customer ID</strong></th>
              <th><strong>Customer Name</strong></th>
              <th><strong>Customer Mobile</strong></th>
              <th><strong>Added Date</strong></th>
            </tr>
          </thead>
          <tbody id="customers-table-body">
          </tbody>

        `;
  tableContainer.appendChild(table);
  gridContainer.appendChild(tableContainer);

  fetch("/latest-customers/")
    .then((response) => {
      if (!response.ok) {
        throw new Error("فشل في جلب بيانات الزبائن!");
      }
      return response.json();
    })
    .then((customers) => {
      const tableBody = document.getElementById("customers-table-body");
      customers.forEach((customer, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
                <td><strong>${index + 1}</strong></td>
                <td>${customer.name}</td>
                <td>${customer.mobile}</td>
                <td>${customer.created_at}</td>

              `;
        tableBody.appendChild(row);
      });
    })
    .catch((error) => {
      console.error("خطأ في جلب بيانات الزبائن:", error);
      alert("حدث خطأ أثناء تحميل بيانات الزبائن!");
    });
}

//Fetch_customer_in_debt_page
document.addEventListener("DOMContentLoaded", function () {
  var customerModal = document.getElementById("customerModal");
  customerModal.addEventListener("show.bs.modal", function (event) {
    var button = event.relatedTarget;
    var itemId = button.getAttribute("data-id");
    document.getElementById("item_id_modal").value = itemId;
    fetch(`/customers_view`)
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
        } else {
          var customerSelect = document.getElementById(
            "customerSelect_debt_modal"
          );
          customerSelect.innerHTML = "";
          data.forEach((customer) => {
            var option = document.createElement("option");
            option.value = customer.id;
            option.textContent = `${customer.first_name} ${customer.second_name}`;
            customerSelect.appendChild(option);
          });
        }
      })
      .catch((error) => {
        console.error("Error fetching item data:", error);
        alert("Failed to fetch item data!");
      });
  });
});

//Fetch_customer_in_Payment_page
document.addEventListener("DOMContentLoaded", function () {
  var paymentModal = document.getElementById("paymentModal");
  paymentModal.addEventListener("show.bs.modal", function (event) {
    var button = event.relatedTarget;
    var itemId = button.getAttribute("data-id");
    document.getElementById("item_id_modal").value = itemId;

    fetch(`/customers_view`)
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
        } else {
          let customerSelect = document.getElementById("customerSelect");
          customerSelect.innerHTML = `<option value="" disabled selected>Select a customer</option>`;
          data.forEach((customer) => {
            var option = document.createElement("option");
            option.value = customer.id;
            option.textContent = `${customer.first_name} ${customer.second_name}`;
            customerSelect.appendChild(option);
          });
        }
      })
      .catch((error) => {
        console.error("Error fetching item data:", error);
        alert("Failed to fetch item data!");
      });
  });
});

//Fetch_debt_in_Payment_page
document.addEventListener("DOMContentLoaded", function () {
document
  .getElementById("customerSelect")
  .addEventListener("change", function () {
    var customerId = this.value;
    fetch(`/debt_view?customer_id=${customerId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
        } else {
          let debtSelect = document.getElementById("debtSelect");
          debtSelect.innerHTML = "";
          data.forEach((debt) => {
            var option = document.createElement("option");
            option.value = debt.id;
            option.textContent = `${debt.amount_debt} ${debt.notes}`;
            debtSelect.appendChild(option);
          });
        }
      })
      .catch((error) => {
        alert("فشل في جلب البيانات!");
      });
  });
});

//add_debts_by_modal
document.addEventListener("DOMContentLoaded", function () {
document
  .querySelector("#add_debts")
  .addEventListener("click", function () {
    var selectedCustomer = document.getElementById(
      "customerSelect_debt_modal"
    ).value;
    var debt_amount = document.getElementById("debt_amount").value;
    var debt_Description =
      document.getElementById("debt_description").value;

    console.log({
      customer_id: selectedCustomer,
      debtamount: debt_amount,
      debtDescription: debt_Description,
    });

    fetch("/add_debts/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector(
          "[name=csrfmiddlewaretoken]"
        ).value,
      },
      body: JSON.stringify({
        customer_id: selectedCustomer,
        debtamount: debt_amount,
        debtDescription: debt_Description,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Debt was updated successfully!");
          location.reload();
          loaddebtspage();
        } else {
          alert("Failed to update item! Error: " + data.error); // إضافة تفاصيل الخطأ
        }
      })
      .catch((error) => {
        console.error("Error updating item:", error);
        alert("Failed to update item!");
      });
  });
});

//add_payment_by_modal
document.addEventListener("DOMContentLoaded", function () {
document
  .querySelector("#savePaymentButton")
  .addEventListener("click", function () {
    var selectedCustomer =
      document.getElementById("customerSelect").value;
    var paymentAmount = document.getElementById("paymentAmount").value;
    var paymentType = document.getElementById("paymentType").value;
    var debtSelect = document.getElementById("debtSelect").value;
    fetch("/add_payment/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector(
          "[name=csrfmiddlewaretoken]"
        ).value,
      },
      body: JSON.stringify({
        customer_id: selectedCustomer,
        payment_amount: paymentAmount,
        payment_type: paymentType,
        debt_id: debtSelect,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Payment was added successfully!");
          location.reload(); // إعادة تحميل الصفحة بعد التحديث
        } else {
          alert(data.error);
        }
      })
      .catch((error) => {
        console.error("Error adding payment:", error);
        alert("Failed to add payment!" + error.message);
      });
  });
});

function deleteCustomer(customerId) {
  if (confirm("Are you sure you want to delete this customer?")) {
    fetch(`/api/customers/delete/${customerId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message === "Customer deleted successfully") {
          alert("Customer deleted successfully");
          // Reload the customer list after deletion
          document.getElementById("customers-link").click();
        } else {
          alert("Failed to delete customer");
        }
      })
      .catch((error) => {
        console.error("Error deleting customer:", error);
        alert("Error deleting customer");
      });
  }
}

// فتح المودال وتعبئة الحقول
function openEditModal(debtId, amount, notes) {
  document.getElementById("editDebtId").value = debtId;
  document.getElementById("editDebtAmount").value = amount;
  document.getElementById("editDebtNotes").value = notes;

  const editModal = new bootstrap.Modal(
    document.getElementById("editDebtModal")
  );
  editModal.show();
}

// حدث الزر لحفظ التعديلات
document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("saveDebtChanges")
    .addEventListener("click", function () {
      const debtId = document.getElementById("editDebtId").value;
      const amount = document.getElementById("editDebtAmount").value;
      const notes = document.getElementById("editDebtNotes").value;
      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      fetch(`/edit_debt/${debtId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          amount_debt: amount,
          notes: notes,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            alert("Debt updated successfully!");
            location.reload(); // تحديث الصفحة
          } else {
            alert(data.error || "Failed to update debt.");
          }
        })
        .catch((error) => {
          console.error("Error updating debt:", error);
          alert("Error updating debt.");
        });
    });
});

// دالة حذف الدين عبر AJAX
document.addEventListener("DOMContentLoaded", function () {
document.addEventListener('click', function (e) {
  if (e.target.classList.contains('delete-btn')) {
    const debtId = e.target.getAttribute('data-id');  // الحصول على معرّف الدين

    if (confirm("Are you sure you want to delete this debt?")) {
      fetch(`/delete_debt/${debtId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,  // استخدام الـ csrfToken الذي تم تعريفه في JavaScript
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: debtId }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert("Debt deleted successfully!");
            e.target.closest('tr').remove();  // حذف الصف من الجدول
          } else {
            alert("Failed to delete the debt.");
          }
        })
        .catch(error => console.error('Error:', error));
    }
  }
});
});


document.addEventListener("DOMContentLoaded", function () {
document
  .querySelectorAll('[data-bs-target="#editCustomerModal"]')
  .forEach((button) => {
    button.addEventListener("click", function () {
      const customerId = this.getAttribute("data-id");
      // جلب بيانات العميل
      fetch(`/api/customers/${customerId}/`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Customer not found");
          }
          return response.json();
        })
        .then((customer) => {
          // ملء الفورم بالبيانات
          document.getElementById("customerId").value = customer.id;
          document.getElementById("firstName").value =
            customer.first_name;
          document.getElementById("secondName").value =
            customer.second_name;
          document.getElementById("email").value = customer.email;
          document.getElementById("mobile").value = customer.mobile;
        })
        .catch((error) => {
          console.error("Error fetching customer data:", error);
          alert("Failed to fetch customer data.");
        });
    });
  });
});

// التعامل مع الفورم عند الإرسال
document.addEventListener("DOMContentLoaded", function () {
document
  .getElementById("editCustomerForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const customerId = document.getElementById("customerId").value;
    const formData = {
      first_name: document.getElementById("firstName").value,
      second_name: document.getElementById("secondName").value,
      email: document.getElementById("email").value,
      mobile: document.getElementById("mobile").value,
    };

    // إرسال البيانات إلى الخادم
    fetch(`/api/customers/${customerId}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        console.log("Response status:", response.status);
        if (!response.ok) {
          return response.json().then((err) => {
            console.error("Error response from server:", err);
            throw new Error("Failed to update customer");
          });
        }
        alert("Customer updated successfully!");
        document.getElementById("customers-link").click();
      })
      .catch((error) => {
        console.error("Error updating customer:", error);
        alert("Failed to update customer.");
      });
  });
});

