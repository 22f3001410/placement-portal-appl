<template>

<div class="container mt-4">

<h2>My Applications</h2>

<!-- Success / Error Messages -->

<div v-if="message" class="alert alert-success">
{{ message }}
</div>

<div v-if="error" class="alert alert-danger">
{{ error }}
</div>

<button class="btn btn-primary mb-3" @click="exportCSV">
Export CSV
</button>

<!-- Loading -->

<div v-if="loading" class="text-center my-3">
Loading applications...
</div>

<!-- Applications Table -->

<table class="table table-hover table-striped" v-if="apps.length">

<thead>
<tr>
<th>Company</th>
<th>Job</th>
<th>Status</th>
<th>Applied On</th>
<th>Interview</th>
</tr>
</thead>

<tbody>

<tr v-for="a in apps" :key="a.id">

<td>{{ a.company }}</td>
<td>{{ a.job_title }}</td>
<td>{{ a.status }}</td>
<td>{{ a.application_date }}</td>
<td>
  {{ a.interview_date ? new Date(a.interview_date).toLocaleString() : "Not Scheduled" }}
</td>

</tr>

</tbody>

</table>

<!-- Empty State -->

<div v-if="!loading && !apps.length" class="text-muted">
No applications yet
</div>


<!-- PROFILE UPDATE SECTION -->

<h3 class="mt-5">Update Profile</h3>

<div class="card p-3">

<input
v-model="profile.name"
class="form-control mb-2"
placeholder="Name"
/>

<input
v-model="profile.branch"
class="form-control mb-2"
placeholder="Branch"
/>

<input
v-model="profile.cgpa"
class="form-control mb-2"
placeholder="CGPA"
/>

<input
v-model="profile.year"
class="form-control mb-2"
placeholder="Year"
/>

<button class="btn btn-success" @click="updateProfile">
Update Profile
</button>

</div>

</div>

</template>


<script>

import api from "../services/api"

export default {

data(){
return{

apps:[],
loading:false,

message:"",
error:"",

profile:{
name:"",
branch:"",
cgpa:"",
year:""
}

}
},

async mounted(){

this.loading = true

try{

const res = await api.get("/student/applications")

this.apps = res.data

}catch(err){

this.error = "Failed to load applications"

}

this.loading = false

},

methods:{

async exportCSV(){

try{

const res = await api.get("/student/export")

const taskId = res.data.task_id

this.message = "Export started. Waiting for completion..."

this.checkTaskStatus(taskId)

}catch(err){

this.error = "Export failed"

}

},

async checkTaskStatus(taskId){

const interval = setInterval(async ()=>{

const res = await api.get("/student/task-status/" + taskId)

if(res.data.state === "SUCCESS"){

clearInterval(interval)

this.message = "CSV export completed!"

}

},2000)

},

async updateProfile(){

try{

await api.put("/student/update-profile", this.profile)

this.message = "Profile updated successfully"

}catch(err){

this.error = "Profile update failed"

}

}

}

}

</script>