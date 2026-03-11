<template>
<DashboardLayout :menuItems="menu">

<div>

<h2 class="mb-4">Admin Dashboard</h2>

<!-- Statistics -->
<div id="stats" class="row mb-4">

<div class="col-md-4">
<div class="card shadow-sm p-3 text-center">
<h5>Total Students</h5>
<h3>{{ stats.total_students }}</h3>
</div>
</div>

<div class="col-md-4">
<div class="card shadow-sm p-3 text-center">
<h5>Total Companies</h5>
<h3>{{ stats.total_companies }}</h3>
</div>
</div>

<div class="col-md-4">
<div class="card shadow-sm p-3 text-center">
<h5>Total Drives</h5>
<h3>{{ stats.total_drives }}</h3>
</div>
</div>

</div>

<!-- Report -->
<div class="card shadow-sm p-4 mb-4">

  <h5>Placement Reports</h5>

  <table class="table table-bordered">

    <tbody>

      <tr>
        <td>Total Applications</td>
        <td>{{ reports.total_applications }}</td>
      </tr>

      <tr>
        <td>Placed Students</td>
        <td>{{ reports.placed_students }}</td>
      </tr>

      <tr>
        <td>Placement Rate</td>
        <td>{{ reports.placement_rate }}%</td>
      </tr>

    </tbody>

  </table>

</div>

<!-- VIEW LISTS -->
<div id="applications" class="card shadow-sm p-4 mb-4">
<h5>View Lists</h5>
<div class="mb-3">
<button class="btn btn-secondary me-2" @click="loadStudents">Students</button>
<button class="btn btn-secondary me-2" @click="loadCompanies">Companies</button>
<button class="btn btn-secondary" @click="loadDrives">Drives</button>
</div>

<table class="table table-striped" v-if="list.length">

<thead>
<tr>
<th>ID</th>
<th>Title</th>
<th v-if="currentView==='companies' || currentView==='drives'">Status</th>
<th v-if="currentView==='companies' || currentView==='drives' || currentView==='students'">Actions</th>
</tr>
</thead>

<tbody>

<tr v-for="item in list" :key="item.id">

<td>{{ item.id }}</td>
<td>
{{ item.name || item.company_name || item.title }}

<span
v-if="item.is_active === false"
class="badge bg-danger ms-2">
Blacklisted
</span>

</td>

<!-- STATUS COLUMN -->

<td v-if="currentView==='companies'">

<span v-if="item.approval_status==='Approved'" class="badge bg-success">
Approved
</span>

<span v-else-if="item.approval_status==='Rejected'" class="badge bg-danger">
Rejected
</span>

<span v-else class="badge bg-warning text-dark">
Pending
</span>

</td>

<td v-if="currentView==='drives'">

<span v-if="item.status==='Approved'" class="badge bg-success">
Approved
</span>

<span v-else-if="item.status==='Rejected'" class="badge bg-danger">
Rejected
</span>

<span v-else class="badge bg-warning text-dark">
Pending
</span>

</td>

<!-- ACTIONS -->

<td v-if="currentView==='companies' || currentView==='drives' || currentView==='students'">

<!-- STUDENT BLACKLIST -->

<button
v-if="currentView==='students'"
class="btn btn-warning btn-sm me-2"
:disabled="item.is_active === false"
@click="deactivateUser(item.user_id)">
Blacklist
</button>

<button
v-if="currentView==='students'"
class="btn btn-success btn-sm"
:disabled="item.is_active === true"
@click="activateUser(item.user_id)">
Activate
</button>

<!-- COMPANY BLACKLIST -->

<button
v-if="currentView==='companies'"
class="btn btn-warning btn-sm me-2"
:disabled="item.is_active === false"
@click="deactivateUser(item.user_id)">
Blacklist
</button>

<button
v-if="currentView==='companies'"
class="btn btn-success btn-sm me-2"
:disabled="item.is_active === true"
@click="activateUser(item.user_id)">
Activate
</button>

<button
v-if="currentView==='companies'"
class="btn btn-success btn-sm me-2"
:disabled="item.approval_status==='Approved' || item.approval_status==='Rejected'"
@click="approveCompany(item.id)"
>
Approve
</button>

<button
v-if="currentView==='companies'"
class="btn btn-danger btn-sm me-2"
:disabled="item.approval_status==='Approved' || item.approval_status==='Rejected'"
@click="rejectCompany(item.id)"
>
Reject
</button>

<button
v-if="currentView==='drives'"
class="btn btn-success btn-sm me-2"
:disabled="item.status==='Approved' || item.status==='Rejected'"
@click="approveDrive(item.id)"
>
Approve
</button>

<button
v-if="currentView==='drives'"
class="btn btn-danger btn-sm"
:disabled="item.status==='Approved' || item.status==='Rejected'"
@click="rejectDrive(item.id)"
>
Reject
</button>

</td>

</tr>

</tbody>
</table>

</div>

<!-- SEARCH COMPANIES -->
<div id="companies" class="card shadow-sm p-4 mb-4">
<h5>Search Companies</h5>

<div class="d-flex gap-2 mb-3">
<input v-model="companySearch" class="form-control" placeholder="Enter company name">
<button class="btn btn-primary" @click="searchCompanies">Search</button>
</div>

<table class="table table-striped" v-if="companies.length">

<thead>
<tr>
<th>ID</th>
<th>Company</th>
<th>Status</th>
<th></th>
</tr>
</thead>

<tbody>

<tr v-for="c in companies" :key="c.id">

<td>{{ c.id }}</td>
<td>{{ c.company_name }}</td>

<td>

<span v-if="c.approval_status==='Approved'" class="badge bg-success">
Approved
</span>

<span v-else-if="c.approval_status==='Rejected'" class="badge bg-danger">
Rejected
</span>

<span v-else class="badge bg-warning text-dark">
Pending
</span>

</td>

<td>

<button
class="btn btn-success btn-sm me-2"
:disabled="c.approval_status==='Approved' || c.approval_status==='Rejected'"
@click="approveCompany(c.id)"
>
Approve
</button>

<button
class="btn btn-danger btn-sm"
:disabled="c.approval_status==='Approved' || c.approval_status==='Rejected'"
@click="rejectCompany(c.id)"
>
Reject
</button>

</td>

</tr>

</tbody>
</table>

</div>

<!-- Search Students -->
<div id="drives" class="card shadow-sm p-4 mb-4">
<h5>Search Students</h5>

<div class="d-flex gap-2 mb-3">

<input
v-model="searchQuery"
class="form-control"
placeholder="Enter student name"
/>

<button
class="btn btn-primary"
@click="searchStudents"
>
Search
</button>

</div>

<table class="table table-striped" v-if="students.length">

<thead>
<tr>
<th>ID</th>
<th>Name</th>
</tr>
</thead>

<tbody>

<tr v-for="s in students" :key="s.id">
<td>{{ s.id }}</td>
<td>{{ s.name }}</td>
</tr>

</tbody>

</table>

</div>

<!-- SEARCH DRIVES -->
<div class="card shadow-sm p-4 mb-4">

<h5>Search Drives</h5>

<div class="d-flex gap-2 mb-3">
<input v-model="driveSearch" class="form-control" placeholder="Enter drive title">
<button class="btn btn-primary" @click="searchDrives">Search</button>
</div>

<table class="table table-striped" v-if="drives.length">

<thead>
<tr>
<th>ID</th>
<th>Title</th>
<th></th>
</tr>
</thead>

<tbody>

<tr v-for="d in drives" :key="d.id">

<td>{{ d.id }}</td>
<td>{{ d.title }}</td>

<td>

<button
class="btn btn-success btn-sm me-2"
:disabled="d.status==='Approved' || d.status==='Rejected'"
@click="approveDrive(d.id)"
>
Approve
</button>

<button
class="btn btn-danger btn-sm"
:disabled="d.status==='Approved' || d.status==='Rejected'"
@click="rejectDrive(d.id)"
>
Reject
</button>

</td>

</tr>

</tbody>

</table>

</div>

</div>

</DashboardLayout>
</template>

<script>

import api from "../services/api"
import DashboardLayout from "../layouts/DashboardLayout.vue"

export default {

components:{DashboardLayout},

data(){
return{

menu: [
  { label: "Dashboard",    ref: "stats" },
  { label: "Companies",    ref: "companies" },
  { label: "Drives",       ref: "drives" },
  { label: "Applications", ref: "applications" }
],

stats:{},
reports:{},

list:[],
companies:[],
drives:[],
students:[],

companySearch:"",
studentQuery:"",
driveSearch:"",

currentView:"companies"

}
},

mounted(){
this.loadStats()
this.loadReports()
this.loadCompanies()
},

methods:{

async loadStats(){
const res = await api.get("/admin/dashboard")
this.stats = res.data
},

async loadStudents(){
const res = await api.get("/admin/students")
this.list = res.data
this.currentView="students"
},

async loadCompanies(){
const res = await api.get("/admin/companies")
this.list = res.data
this.currentView="companies"
},

async loadDrives(){
const res = await api.get("/admin/drives")
this.list = res.data
this.currentView="drives"
},

async searchCompanies(){

if(!this.companySearch){
this.companies=[]
return
}

const res = await api.get(`/admin/search/companies?name=${this.companySearch}`)
this.companies=res.data

},

async searchStudents(){

if(!this.searchQuery){
this.students=[]
return
}

const res = await api.get(`/admin/search/students?name=${this.searchQuery}`)
this.students = res.data

},

async searchDrives(){

if(!this.driveSearch){
this.drives=[]
return
}

const res = await api.get(`/admin/search/drives?title=${this.driveSearch}`)
this.drives=res.data

},

async approveCompany(id){
await api.put(`/admin/approve-company/${id}`)
this.loadCompanies()
},

async rejectCompany(id){
await api.put(`/admin/reject-company/${id}`)
this.loadCompanies()
},

async approveDrive(id){
await api.put(`/admin/approve-drive/${id}`)
this.loadDrives()
},

async rejectDrive(id){
await api.put(`/admin/reject-drive/${id}`)
this.loadDrives()
},

async deactivateUser(id){

await api.put(`/admin/deactivate-user/${id}`)

if(this.currentView === "students"){
  this.loadStudents()
}

if(this.currentView === "companies"){
  this.loadCompanies()
}

},

async activateUser(id){

await api.put(`/admin/activate-user/${id}`)

if(this.currentView === "students"){
  this.loadStudents()
}

if(this.currentView === "companies"){
  this.loadCompanies()
}

},

async deactivateUser(id){

if(!confirm("Are you sure you want to blacklist this user?")){
return
}

await api.put(`/admin/deactivate-user/${id}`)
this.loadStudents()
this.loadCompanies()

},

async loadReports(){
const res = await api.get("/admin/reports")
this.reports = res.data
}

}

}

</script>