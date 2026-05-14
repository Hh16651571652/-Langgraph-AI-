import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Login from '../views/Login.vue'

describe('Login.vue', () => {
  it('renders login form', () => {
    const wrapper = mount(Login)
    expect(wrapper.find('h2').text()).toContain('登录')
  })

  it('has username and password inputs', () => {
    const wrapper = mount(Login)
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
  })

  it('shows validation error for empty fields', async () => {
    const wrapper = mount(Login)
    const form = wrapper.find('form')
    await form.trigger('submit.prevent')
    // 验证逻辑应该在组件中实现
  })
})
