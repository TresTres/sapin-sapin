
<template>
  <Activity>
    <template #header>User Financial Data</template>
    <template #bar>
      <div class="activity-form-toggle">
        <ActivityForm
          title="Create Data Series"
          button-title="Create"
          :style="{ display: showActivityForm ? 'block' : 'none' }"
          @submit="handleSeriesCreation"
        >
          <ActivityFormInput
            v-model:inputValue="seriesTitle"
            :label="seriesTitleLabel"
            :index="0"
            placeholder="Monthly Grocery Budget"
          />
        </ActivityForm>
      </div>
      <button
        type="button"
        class="activity-form-toggle-button"
        @click.prevent="toggleActivityForm"
      >
        {{ showActivityFormText }}
      </button>
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

  const dataStore = useDataStore();
  const dataSeries = await useAuthorizingFetch("/api/data/series");
  dataStore.loadSeries(dataSeries);

  const showActivityForm = ref(false);
  const showActivityFormText = ref("Create Data Series");

  const seriesTitleLabel = "New Series Title";
  const seriesDescriptionLabel = "New Series Description";
  const seriesTitle = ref("");
  const description = ref("");

  const handleSeriesCreation = async (): Promise<void> => {
    const response = await useAuthorizingFetch("/api/data/series", {
      method: "POST",
      body: JSON.stringify({
        title: seriesTitle.value,
        description: description.value,
      }),
    });
    console.log(response);
  };

  const toggleActivityForm = () => {
    showActivityForm.value = !showActivityForm.value;
    showActivityFormText.value = !!showActivityForm.value
      ? "Hide Form"
      : "Create Data Series";
  };
</script>
