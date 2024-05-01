<template>
  <Activity>
    <template #header>
      <h2>{{ series?.title || "" }}</h2>
      <p>{{ series?.description || "" }}</p>
    </template>
    <template #content>
      <div className="graph-area"></div>

      <div className="cells-area"></div>

      <div className="edit-area"></div>
    </template>
  </Activity>
</template>

<script lang="ts" setup>
  definePageMeta({
    title: `User Series`,
    layout: "dashboard",
  });

  const route = useRoute();
  const dataStore = useDataStore();
  let series: DataEventSeries | undefined = undefined;

  //retrieve series data
  onBeforeMount(() => {
    series = dataStore.getSeries(route.params.slug as string);
    console.log(series);
  });
</script>
