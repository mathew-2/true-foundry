A **service** to convert hugging face input into V2 input protocol (used by true foundry) and output the results.

## Models available are:
        - zero-shot-model: https://zero-shot-model-intern-mathew.demo1.truefoundry.com
        - test-object-detect: https://test-object-detect-intern-mathew.demo1.truefoundry.com
        - text-gen-model:  https://text-gen-model-intern-mathew.demo1.truefoundry.com \\ currently deployed
        - token-class-model: https://token-class-model-intern-mathew.demo1.truefoundry.com

## How to use?
Sample Input for text-gen-model: 
```
{
  "hf_pipeline": "text-gen-model",
  "model_deployed_url": "https://text-gen-model-intern-mathew.demo1.truefoundry.com",
  "inputs": "tell me what",
  "parameters": ""
}
```

Sample Input for test-object-detect:
``` 
{
  "hf_pipeline": "test-object-detect",
  "model_deployed_url": "https://test-object-detect-intern-mathew.demo1.truefoundry.com",
  "inputs": "sample.png", # converting local image in PIL object and passing it as input
  "parameters": ""
}
{
  "hf_pipeline": "test-object-detect",
  "model_deployed_url": "https://test-object-detect-intern-mathew.demo1.truefoundry.com",
  "inputs": "https://pixabay.com/get/g449eda9816dd2e2d6770bb74318350cf7b3e86e2f00c17ce061f7fa75fab878584b03d9dddaea433513f412bd315a8eb1b402f89fbc55e634f3236408a496715890f436b485526958da8415416b393de_640.jpg", 
  "parameters": ""
}
```


       
