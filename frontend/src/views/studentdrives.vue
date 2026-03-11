<template>

<div class="container mt-4">

<h2>Available Placement Drives</h2>
<div v-if="message" class="alert alert-success">
{{ message }}
</div>

<div v-if="error" class="alert alert-danger">
{{ error }}
</div>

<div v-if="loading" class="text-center my-3">
Loading drives...
</div>

<input v-model="search" class="form-control mb-3" placeholder="Search Drives">

<table class="table">

<thead>
<tr>
<th>Company</th>
<th>Job Title</th>
<th>CGPA</th>
<th>Deadline</th>
<th></th>
</tr>
</thead>

<tbody>

<tr v-for="d in filteredDrives" :key="d.id">

<td>{{ d.company_name }}</td>
<td>{{ d.title }}</td>
<td>{{ d.min_cgpa }}</td>
<td>{{ d.eligible_branch }}</td>
<td>{{ new Date(d.deadline).toLocaleDateString() }}</td>

<td>
<button class="btn btn-success btn-sm" @click="apply(d.id)">
Apply
</button>
</td>

</tr>

</tbody>

</table>

</div>

</template>

<script>
import api from "../services/api"

export default {

data(){
return{
drives:[],
search:"",
message:"",
error:""
}
},

computed:{
filteredDrives(){
return this.drives.filter(d =>
d.title.toLowerCase().includes(this.search.toLowerCase())
)
}
},

async mounted(){

this.loading = true

try{

const res = await api.get("/student/dashboard")
this.drives = res.data

}catch(err){

this.error = "Failed to load drives"

}

this.loading = false

},

methods:{

async apply(id){

try{

await api.post(`/student/apply/${id}`)

this.message = "Application submitted successfully"

}catch(err){

this.error = "Application failed"

}

}

}

}
</script>