import { mountSuspended } from "@nuxt/test-utils/runtime";
import type { DOMWrapper } from "@vue/test-utils";
import { describe, it, expect } from "vitest";

import Navbar from "@/components/Navbar.vue";

describe("Navbar component", () => {
  it("should prepare a NuxtLink for each route", async () => {
    const routeProps = [
      { name: "Foo", path: "/foo" },
      { name: "Bar", path: "/bar" },
    ];

    const navbarComponent = await mountSuspended(Navbar, {
      props: {
        routes: routeProps,
      },
    });
    const navList = navbarComponent.find("ul");
    const linkItems = navList.findAll("li");

    expect(linkItems).toHaveLength(routeProps.length);
    routeProps.forEach((route) => {
      const linkItem = linkItems.find((linkItem) => {
        return linkItem.text() === route.name;
      });
      expect(linkItem).not.toBeUndefined();
      const link = (linkItem as DOMWrapper<any>).find("a");
      expect(link.attributes("href")).toBe(`/${route.path}`);
    });
  });
});
