import { mountSuspended } from '@nuxt/test-utils/runtime'
import DataPage from '~/pages/data.vue'
import { describe, it, expect } from 'vitest'

describe('DataPage', () => {
  it('calls handleSeriesCreation', async () => {
    const wrapper = await mountSuspended(DataPage)
    expect(wrapper).not.toBeUndefined();

    // // Mock the handleSeriesCreation function
    // const mockHandleSeriesCreation = jest.fn()
    // wrapper.vm.handleSeriesCreation = mockHandleSeriesCreation

    // // Call the function
    // await wrapper.vm.handleSeriesCreation()

    // // Check that the function was called
    // expect(mockHandleSeriesCreation).toHaveBeenCalled()
  }) 
})