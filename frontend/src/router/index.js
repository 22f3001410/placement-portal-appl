import { createRouter, createWebHistory } from "vue-router"

import Login from "../views/login.vue"
import RegisterStudent from "../views/registerstudent.vue"
import RegisterCompany from "../views/registercompany.vue"
import AdminDashboard from "../views/admindashboard.vue"
import CompanyDashboard from "../views/companydashboard.vue"
import StudentDashboard from "../views/studentdashboard.vue"
import StudentDrives from "../views/studentdrives.vue"
import StudentApplications from "../views/studentapplications.vue"
import CompanyDrives from "../views/companydrives.vue"
import CompanyApplications from "../views/companyapplications.vue"
import AdminApprovals from "../views/adminapprovals.vue"

const routes = [
  { path: "/", component: Login },
  { path: "/register-student", component: RegisterStudent },
  { path: "/register-company", component: RegisterCompany },
  { path: "/admin", component: AdminDashboard },
  { path: "/company", component: CompanyDashboard },
  { path: "/student", component: StudentDashboard },
  { path: "/student/drives", component: StudentDrives },
  { path: "/student/applications", component: StudentApplications },
  { path: "/company/drives", component: CompanyDrives },
  { path: "/company/applications", component: CompanyApplications },
  { path: "/admin/approvals", component: AdminApprovals }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")

  if (!token && !["/", "/register-student", "/register-company"].includes(to.path)) {
  return "/"
}

  if (token) {
  if (to.path.startsWith("/admin") && role !== "admin") return "/"
  if (to.path.startsWith("/company") && role !== "company") return "/"
  if (to.path.startsWith("/student") && role !== "student") return "/"
  }

  return true
})

export default router