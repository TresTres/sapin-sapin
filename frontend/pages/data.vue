<template>
  <Activity>
    <template #header>User Financial Data</template>
    <template #bar>
      <button
        type="button"
        class="activity-form-toggle-button"
        @click.prevent="toggleActivityForm"
      >
        {{ showActivityFormText }}
      </button>
      <div class="activity-form-toggle">
        <ActivityForm
          :style="{ display: showActivityForm ? 'block' : 'none' }"
          :banner-text="bannerError"
          title="Create Data Series"
          button-title="Create"
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
    </template>
    <template #content>
      <ul>
        <li v-for="[title, series] of dataStore.allSeries" :key="series.id">
          {{ series.title + " - " + series.id }}
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
  //prepare activity
  const showActivityForm = ref(false);
  const showActivityFormText = ref("Create Data Series");
  //prepare series creation form
  const seriesTitleLabel = "New Series Title";
  const seriesDescriptionLabel = "New Series Description";
  const seriesTitle = ref("");
  const description = ref("");
  const bannerError = ref("");
  //get series
  const dataStore = useDataStore();
  const { owned_series } = await useAuthorizingFetch("/api/data/series");
  dataStore.loadMultipleSeries(owned_series as DataEventSeries[]);

  const handleSeriesCreation = async (): Promise<void> => {
    /*
     * Attempt to create a new data series, and display an error if the series cannot be created.
     */
    if (dataStore.doesSeriesExist(seriesTitle.value)) {
      bannerError.value = "Series already exists";
      return;
    }
    // update UI
    const proposedSeries: DataEventSeries = {
      id: "-0",
      title: seriesTitle.value,
      description: description.value,
    };
    dataStore.addSeries(proposedSeries);
    // POST to server
    await useAuthorizingFetch("/api/data/series", {
      method: "POST",
      body: JSON.stringify(proposedSeries),
    })
    .then((response) => {
      // replace element on success and cleanup
      console.log(response);
      dataStore.replaceSeries(response as DataEventSeries);
      showActivityForm.value = false;
      showActivityFormText.value = "Create Data Series";
      seriesTitle.value = "";
    })
    .catch((error) => {
      // display error in form banner
      console.log(error);
      if (error.data) {
        const { message } = error.data;
        bannerError.value = message;
        return;
      }
      bannerError.value = error;
    });
  };

  const toggleActivityForm = () => {
    showActivityForm.value = !showActivityForm.value;
    showActivityFormText.value = !!showActivityForm.value
      ? "Hide Form"
      : "Create Data Series";
  };
</script>
