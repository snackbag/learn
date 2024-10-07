export default class ComponentLoader {
  constructor (dir) {
      this.dir = dir;
  }

  async renderComponent(element) {
    const tagName = element.tagName.toLowerCase();
    const properties = await this.getProperties(tagName);

    const info = properties['info'];
    const attributes = properties['attributes'];

    const componentHTML = await this.getPresetHTML(info['name']);
    let transformHTML = componentHTML.split("<!---- TRANSFORM ---->")[1];

    for (const attribute in attributes) {
        if (attributes[attribute]['required']) {
            if (!element.hasAttribute(attribute)) {
                console.error('Component \'' + tagName + '\' does not contain required attribute ' + attribute);
                return;
            }
        }

        if (element.hasAttribute(attribute)) {
            transformHTML = transformHTML.replace('//' + attribute + '\\\\', () => element.getAttribute(attribute));
        } else {
            transformHTML = transformHTML.replace('//' + attribute + '\\\\', () => attributes[attribute]['value']);
        }
    }

    element.innerHTML = transformHTML;
  }

  async getProperties(name) {
    const response = await fetch(`${this.dir}/${name}.json`);
    return response.json();
  }

  async getPresetHTML(name) {
    const response = await fetch(`${this.dir}/${name}.html`);
    return response.text();
  }
}