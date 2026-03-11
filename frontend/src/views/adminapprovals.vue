<template>

<div class="container mt-4">

<h2>Company Approvals</h2>

<table class="table">

<tr v-for="c in companies" :key="c.id">

<td>{{ c.name }}</td>

<td>

<button class="btn btn-success btn-sm" @click="approve(c.id)">
Approve
</button>

<button class="btn btn-danger btn-sm" @click="reject(c.id)">
Reject
</button>

</td>

</tr>

</table>

</div>

</template>

<script>

import api from "../services/api"

export default{

data(){
return{
companies:[]
}
},

async mounted(){

const res = await api.get("/admin/companies")

this.companies = res.data

},

methods:{

async approve(id){

await api.post("/admin/company/approve",{id})

location.reload()

},

async reject(id){

await api.post("/admin/company/reject",{id})

location.reload()

}

}

}

</script>