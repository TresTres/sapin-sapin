<template>
    <div>
        <h1>User Financial Data</h1>
        <div v-if="dataStore.isLoading"> 
            Loading...
        </div>
        <div v-else>
            <ul>
                <li v-for="series in dataStore.series" :key="series.id">
                    {{ series.title }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script lang=ts setup>
definePageMeta({
    title: 'User Financial Data',
    layout: 'dashboard'
});

const dataStore = getDataStore();
await dataStore.loadForUser();

</script>