import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Todo from '../views/Todo.vue'

describe('Todo.vue', () => {
  it('renders todo component', () => {
    const wrapper = mount(Todo)
    expect(wrapper.exists()).toBe(true)
  })

  it('has add todo button', () => {
    const wrapper = mount(Todo)
    expect(wrapper.find('button').exists()).toBe(true)
  })
})
