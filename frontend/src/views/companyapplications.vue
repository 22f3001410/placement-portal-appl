<template>

<div class="container mt-4">

<h2>Applicants</h2>

<table class="table">

<thead>
<tr>
<th>Student</th>
<th>Drive</th>
<th>Status</th>
<th>Update</th>
</tr>
</thead>

<tbody>

<tr v-for="a in apps" :key="a.id">

<td>{{ a.student }}</td>
<td>{{ a.drive }}</td>

<td>{{ a.status }}</td>

<td>

<select v-model="a.status" @change="update(a)">
<option>Applied</option>
<option>Shortlisted</option>
<option>Selected</option>
<option>Rejected</option>
</select>

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
apps:[]
}
},

async mounted(){

const res = await api.get("/company/applications")

this.apps = res.data

},

methods:{

async update(app){

await api.put(`/company/application/${app.id}/update`,{status:app.status})

}

}

}

</script>