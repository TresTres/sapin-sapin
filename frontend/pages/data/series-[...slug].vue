<template>
  <Activity>
    <template #header>
      <h2>{{ series?.title || "" }}</h2>
      <p>{{ series?.description || "" }}</p>
    </template>
    <template #content>
      <div class="content-container">
        <CommonCard class="edit-area">
          <ActivityForm
            v-bind="{
              title: 'Add Financial Transaction',
              buttonTitle: 'Create',
              bannerText: bannerError,
            }"
            @submit.prevent="handleSave"
          >
            <ActivityFormInput
              v-model:inputValue="dataPoint.label"
              v-bind="{
                label: 'Label',
                placeholder: 'Grocery Trip',
                required: true,
              }"
            />
            <ActivityFormDatetimeInput
              v-model:dateValue="dataPoint.date"
              label="Date"
              v-bind="{
                placeholder: '2010-10-10',
                required: true,
              }"
            />
            <ActivityFormAmountInput
                  v-model:amountValue="dataPoint.amount"
                  label="Amount"
                  v-bind="{
                    placeholder: '0',
                    required: true,
                  }"
                />

            <ActivityFormInput
              v-model:inputValue="dataPoint.description"
              label="Description"
              v-bind="{
                placeholder: 'Description',
                inputType: FormInputType.AREA,
                required: false,
              }"
            />
            <template #buttons>
              <button
                class="clear-fields-button"
                @click.stop.prevent="resetDataPoint()"
              >
                Clear Fields
              </button>
            </template>
          </ActivityForm>
        </CommonCard>
        <CommonCard class="events-area">
          <ul>
            <li v-for="event in series?.events" :key="event.label">
              <div class="event-box">
                <h3>{{ event.label }}</h3>
                <p>{{ event.description }}</p>
                <p>{{ event.amount }}</p>
                <p>{{ event.date }}</p>
              </div>
            </li>
          </ul>
        </CommonCard>
        <div className="graph-area"></div>
      </div>
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
  let series: DataEventSeries | null;

  //data event addition form
  const bannerError = ref("");
  const dataPoint = ref<DataEvent>({
    label: "",
    description: "",
    date: new Date(),
    amount: 0.0,
  });

  //retrieve series data
  onBeforeMount(() => {
    series = dataStore.getSeries(route.params.slug as string);
  });

  const handleSave = async (): Promise<void> => {
    /*
     * Attempt to add a new data point to the series, and display an error if the data point cannot be added.
     */
    

    if(!checkPointUniqueness()) {
      bannerError.value = "Data point with that name already exists";
      return;
    }
    //update UI
    bannerError.value = "";
    (series as DataEventSeries).events.push(unref(dataPoint.value));
    //POST to server
    await useAuthorizingFetch("/api/data/batch", {
      method: "POST", 
      body: JSON.stringify({
        series_id: (series as DataEventSeries).id,
        data: [unref(dataPoint)]
      }),
    })
      .then((response) => {
        // replace element on success and cleanup
        console.log(response);
        // dataStore.replaceSeries(
        //   proposedSeries.title,
        //   response as DataEventSeries
        // );
        resetDataPoint();
      })
      .catch((error) => {
        // remove element on failure
        (series as DataEventSeries).events.pop();
        // display error in form banner
        if (error.data) {
          const { message } = error.data;
          bannerError.value = message;
          return;
        }
        bannerError.value = error;
      });
  };

  const checkPointUniqueness = () => {
    /*
     * Check if the data point is unique within the series.
     */
    return !(series as DataEventSeries).events.some(
      (event) =>
        event.label === dataPoint.value.label &&
        event.date === dataPoint.value.date
    );
  };

  const resetDataPoint = () => {
    /*
     * Reset the data point ref, clearing all connected form fields.
     */
    dataPoint.value = {
      label: "",
      description: "",
      date: new Date(),
      amount: 0.0,
    };
  };
</script>

<style lang="scss" scoped>
  .content-container {
    display: grid;
    width: 100%;
    height: 100%;
    align-items: stretch;

    grid-template-columns: repeat(15, 1fr);
    grid-template-rows: repeat(9, 1fr);

    gap: 2rem;

    padding: $standard-text-size;

    grid-template-areas:
      "C C C C C  B B B B B  B B B B B B"
      "C C C C C  B B B B B  B B B B B B"
      "C C C C C  B B B B B  B B B B B B"
      "A A A A A  B B B B B  B B B B B B"
      "A A A A A  B B B B B  B B B B B B"
      "A A A A A  B B B B B  B B B B B B"
      "A A A A A  B B B B B  B B B B B B"
      "A A A A A  B B B B B  B B B B B B"
      "A A A A A  B B B B B  B B B B B B";
  }

  .edit-area {
    grid-area: A;
  }

  .events-area {
    grid-area: B;
    width: 100%;

    display: flex;
    flex-direction: column;
    li {
      list-style: none;
    }
  }


  .small-fields {
    border: none;
    display: flex;
    flex-direction: row;
    align-items: stretch;

    gap: $small-text-size;
  }

  .clear-fields-button {
    @include large-button;

    width: 30%;
    left: 0;

    background-color: $dark-red-color;
    color: $white-color;

    &:hover {
      background-color: $light-red-color;
      color: $dark-red-color;
    }
  }
</style>
