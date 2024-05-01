<template>
    <Activity>
        <template #header>
            <h2>{{"PROP GOES HERE"}}</h2>
        </template>
        <template #content>
            <div className="graph-area">
            </div>

            <div className="cells-area">
            </div>

            <div className="edit-area"> 
            </div>


        </template>
    </Activity>
</template>

<script setup lange="ts">
  const route = useRoute();
  definePageMeta({
    title: `User Series`,
    layout: "dashboard",
  });

</script>