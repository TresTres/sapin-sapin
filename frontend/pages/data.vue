<template>
    <Activity>
        <template #header>
            User Financial Data
        </template>
        <template #content>
            <div>
                <ul>
                    <li v-for="series in dataStore.series" :key="series.id">
                        {{ series.title }}
                    </li>
                </ul>
            </div>        
        </template>
    </Activity>
</template>

<script lang=ts setup>
import { useAuthorizingFetch } from '~/composables/authorizingFetch';

definePageMeta({
    title: 'User Financial Data',
    layout: 'dashboard'
});

const dataStore = getDataStore();
const dataSeries = await useAuthorizingFetch('/api/data/series');
dataStore.loadSeries(dataSeries);

</script>