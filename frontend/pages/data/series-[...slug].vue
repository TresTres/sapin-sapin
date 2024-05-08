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
              title: 'Add Data Series',
              buttonTitle: 'Save All',
              bannerText: bannerError,
              descriptionValue: 'Add new data points.',
            }"
            @submit.prevent="handleSaveAll"
          >
            <div class="node-container">
              <fieldset
                class="node"
                v-for="(point, index) in dataPoints"
                :key="point.fieldSetId"
              >
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
                  class="remove-node-button"
                  v-if="dataPoints.length > 1"
                  @click.stop.prevent="removeNode(index)"
                >
                  X
                </button>
              </fieldset>
              <button class="add-node-button" @click.stop.prevent="addNode()">+</button>
            </div>
          </ActivityForm>
        </CommonCard>
        <div className="graph-area"></div>
        <div className="cells-area"></div>
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
  };

  const bannerError = ref("");
  const dataPoints = ref<DataEventProps[]>([
    {
      fieldSetId: 0,
      data: {
        label: "",
        description: "",
        date: new Date(),
        amount: 0,
      },
    },
  ]);

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

  .node-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
  }

  .node {
    width: 100%;
    border: dashed red;

    position: relative;

    .remove-node-button {
      @include small-button;

      position: absolute;
      top: 0;
      right: 0;
      max-height: 1.9em;
      

      background-color: $dark-red-color;
      color: $white-color;

      &:hover {
        background-color: $light-red-color;
        color: $dark-red-color;
      }
    }

  }

  
  .add-node-button {
      @include large-button;

      width: 100%;
      font-size: $large-text-size;
      font-weight: $bold-text-weight;

      background-color: $primary-orange-color;
      color: $dark-red-color;

      &:hover {
        background-color: $light-orange-color;
        color: $dark-red-color;
      }
    }
</style>
