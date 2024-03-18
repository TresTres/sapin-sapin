<template>
  <Activity>
    <template #header> User Financial Data </template>
    <template #bar>
      <div class="activity-form-toggle">
        <ActivityForm title="Create Data Series" :style="{ display: showActivityForm ? 'block' : 'none' }">
          <ActivityFormInput />
        </ActivityForm>
      </div>
      <button type="button" class="activity-form-toggle-button" @click.prevent="toggleActivityForm">{{ showActivityFormText }}</button>
    </template>
    <template #content>
      <ul>
        <li v-for="series in dataStore.series" :key="series.id">
          {{ series.title }}
        </li>
      </ul>
    </template>
  </Activity>
</template>

<script lang="ts" setup>
  definePageMeta({
    title: "User Financial Data",
    layout: "dashboard",
  });

  const dataStore = getDataStore();
  const dataSeries = await useAuthorizingFetch("/api/data/series");
  dataStore.loadSeries(dataSeries);

  const showActivityForm = ref(false);
  const showActivityFormText = ref("Create Data Series")

  const toggleActivityForm = () => {
    showActivityForm.value = !showActivityForm.value;
    showActivityFormText.value = !!(showActivityForm.value) ? "Hide Form" : "Create Data Series" ;
  };


</script>
