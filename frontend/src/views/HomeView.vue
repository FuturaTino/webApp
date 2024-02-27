<script setup>
import Capture from '@/components/Capture.vue';
import captures from '@/data/captures.json';
import {RouterView} from 'vue-router';
import {ref} from 'vue';
import CreateCapture from "@/components/CreateCapture.vue";


const show_Modal = ref(false);

const toggleModal = () => {
    show_Modal.value =!show_Modal.value;
}

// verify the token.
</script>

<template>

<h1>HomeView</h1>
<div class="container">
    <CreateCapture v-if="show_Modal" @close="toggleModal()" @notShowModal="toggleModal()"/>
    <div class="search-box">
        <div>
            <label for="Search">Search:</label>
        <input type="text" id="Search" placeholder="Search..."/>
        </div>
        <button id="create" class="create" @click="toggleModal()" >创建</button>
    </div>
    <div class="list-box">
        <Capture v-for="capture in captures" :key="capture.id" :capture="capture"/>
    </div>

</div>
</template>

<style scoped>
    .container {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        flex-direction: column;

        justify-content: flex-start;
        margin:auto;
    }
    .container .search-box {
        display: flex;
        justify-content:space-evenly;

    }

    .search-box label {
        font-weight: bold;
        margin-right: 10px;
    }

    .search-box input {
        border: none;
        background-color: rgba(128,128,128, 0.1);
        padding: 10px;
        border-radius: 5px;
    }
    .list-box {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 2%;
    }
</style>
