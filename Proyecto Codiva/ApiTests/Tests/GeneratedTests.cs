Here is the OpenAPI specification for the MovR API:

* `openapi` field: This specifies the version of the OpenAPI specification being used, which in this case is 3.0.2.
* `info`: This section contains metadata about the API, such as its title and description. In this case, the title is "MovR API" and the description is a brief overview of the API.
* `servers`: This section specifies the base URLs for each server where the API can be accessed. In this case, there is only one server with the URL "https://movr-api.herokuapp.com".
* `paths`: This section defines the endpoints and operations that are available in the API. There are several paths defined here, including "/users", "/sessions", and "/clubs". Each path specifies a request method (e.g., GET, POST, PUT, DELETE) and a summary of what the endpoint does.
* `components`: This section defines the reusable components that can be used throughout the API specification. In this case, there is only one component defined: "schemas". This specifies the definitions for the request bodies and responses for each endpoint in the API.
* `securitySchemes`: This section defines the security schemes that are used to secure the API. In this case, there are two security schemes defined: "Bearer" and "ApiKey". These can be used to specify which types of authentication are required for each endpoint.
* `tags`: This section defines the tags that can be used to categorize the endpoints in the API. In this case, there are 14 different tags defined, such as "Application Settings", "Authentication", and "BlockedActions". These can be used to group related endpoints together for easier navigation.

Overall, this OpenAPI specification provides a clear and detailed description of the MovR API, including its endpoints, request methods, parameters, response bodies, and security schemes. It can be used to generate documentation, test clients, and even automate testing for the API.