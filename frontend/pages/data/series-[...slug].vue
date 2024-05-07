<template>
  <Activity>
    <template #header>
      <h2>{{ series?.title || "" }}</h2>
      <p>{{ series?.description || "" }}</p>
    </template>
    <template #content>
      <div class="content-container">
        <div className="graph-area"></div>

        <div className="cells-area"></div>

        <CommonCard class="edit-area">
          <ActivityForm
            v-bind="{
              title: 'Add Data Series',
              buttonTitle: 'Save All',
              bannerText: bannerError,
              descriptionValue: 'Add new data points.',
            }"
            @submit.prevent="handleSaveAll"
          >
            <div class="node-container">
              <div
                v-for="(point, index) in dataPoints"
                :key="point.fieldSetId"
              >
                <fieldset class="node">
                  <ActivityFormInput
                    @update:inputValue="point.data.label = $event"
                    label="Data Label"
                    v-bind="{
                      index,
                      placeholder: 'Label',
                      required: true,
                      inputValue: point.data.label,
                    }"
                  />
                  <button
                    v-if="dataPoints.length > 1"
                    @click.stop.prevent="removeNode(index)"
                  >
                    x
                  </button>
                </fieldset>
              </div>
              <button @click.stop.prevent="addNode()">+</button>
            </div>
          </ActivityForm>
        </CommonCard>
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
  let series: DataEventSeries | null = null;

  //data event addition form

  type DataEventProps = {
    fieldSetId: number;
    data: DataEvent;
  }

  const bannerError = ref("");
  const dataPoints = ref<DataEventProps[]>([{
    fieldSetId: 0,
    data: {
      label: "",
      description: "",
      date: new Date(),
      amount: 0,
    },
  }]);

  //retrieve series data
  onBeforeMount(() => {
    series = dataStore.getSeries(route.params.slug as string);
  });

  const addNode = () => {
    dataPoints.value.push({
      fieldSetId: dataPoints.value.length,
      data: {
        label: "",
        description: "",
        date: new Date(),
        amount: 0,
      },
    });
  };

  const removeNode = (ind: number) => {
    dataPoints.value.splice(ind, 1);
    console.log(dataPoints.value);
  };

  const handleSaveAll = () => {
    console.log(dataPoints.value);
  };
</script>

<style lang="scss" scoped>
  .content-container {
    display: grid;
    width: 100%;
    height: 100%;
    align-items: stretch;

    grid-template-columns: repeat(16, 1fr);
    grid-template-rows: repeat(10, 1fr);

    gap: 2rem;

    padding: $standard-text-size;

    grid-template-areas:
      "A A A A  A B B B  B B B B  B B B B"
      "A A A A  A B B B  B B B B  B B B B"
      "A A A A  A B B B  B B B B  B B B B"
      "A A A A  A B B B  B B B B  B B B B"
      "A A A A  A B B B  B B B B  B B B B"
      "A A A A  A B B B  B B B B  B B B B"
      "A A A A  A C C C  C C C C  C C C C"
      "A A A A  A C C C  C C C C  C C C C"
      "A A A A  A C C C  C C C C  C C C C"
      "A A A A  A C C C  C C C C  C C C C";
  }

  .edit-area {
    grid-area: A;
  }
</style>
