import { shallowMount } from "@vue/test-utils";
import { describe, it, expect } from "vitest";

import ActivityShell from "~/components/activity/ActivityShell.vue";
import { Html } from "../../.nuxt/components";

describe("Activity", () => {
  it("Places activity content into an overlay component correctly", () => {
    const wrapper = shallowMount(ActivityShell, {
      slots: {
        header: "Activity Name",
        bar: "<div>Bar</div>",
        content: "<div>Content</div>",
      },
    });

    const wrapperHeader = wrapper.find("h1");
    expect(wrapperHeader.text()).toBe("Activity Name");
    const wrapperActivityContainer = wrapper.find(".activity-container");
    expect(wrapperActivityContainer.element.children).toHaveLength(2);
    const wrapperBar = wrapper.find(".activity-bar");
    expect(wrapperBar.element).toBe(
      wrapperActivityContainer.element.children[0],
    );
    expect(wrapperBar.text()).toBe("Bar");
    expect(wrapperActivityContainer.element.children[1].textContent).toBe(
      "Content",
    );
  });
});
