# ms-request-tester
Python module to test Moleculer Services endpoints (or any REST API)

#### Using a JSON configurarion file, test your REST API endpoints.

**Resources** Correspond to API endponts. Ex: https://some-domain/api/<resource>
Nested inside *resources*, set the *REST* actions and the data they need to be tested. Ex: *create*, *update*, etc.

**Example file:**

```
{
  "api_url": "<api-root-url>",
  "headers": {
    "A-Header": "<header-value>"
  },
  "resources": {
    "<resource-name>": {
      "<action-name>": {
        "<action-param-1>": "<action-parama-value-1",
        "<action-param-2>": "<action-parama-value-3"
      }
    }
  }
}

```
