//  Need to install the ONNXRUNTIME framework


//  Example from ONNXRUNTIME documentation
#include "onnxruntime_cxx_api.h"
// Load the model and create InferenceSession
Ort::Env env;
std::string model_path = "path/to/your/onnx/model";
Ort::Session session(env, model_path, Ort::SessionOptions{ nullptr });
// Load and preprocess the input image to inputTensor
...
// Run inference
std::vector outputTensors =
session.Run(Ort::RunOptions{nullptr}, inputNames.data(), &inputTensor, 
  inputNames.size(), outputNames.data(), outputNames.size());
const float* outputDataPtr = outputTensors[0].GetTensorMutableData();
std::cout << outputDataPtr[0] << std::endl;



// ChatGPT response Not implemented correctly :)

#include <onnxruntime/core/session/onnxruntime_cxx_api.h>

Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "test");
Ort::SessionOptions session_options;
session_options.SetIntraOpNumThreads(1);

// Assuming you have a path to the ONNX model file
const std::string model_path = "path_to_model.onnx";

Ort::Session session(env, model_path.c_str(), session_options);

// Print model input layer (node names, types, shapes)
Ort::AllocatorWithDefaultOptions allocator;
size_t num_input_nodes = session.GetInputCount();
std::vector<const char*> input_node_names(num_input_nodes);
std::vector<int64_t> input_node_dims;

for (std::size_t i = 0; i < num_input_nodes; i++) {
  // print input node names
  char* input_name = session.GetInputName(i, allocator);
  std::cout << "Input " << i << " : name=" << input_name << std::endl;
  input_node_names[i] = input_name;

  // print input node types
  Ort::TypeInfo type_info = session.GetInputTypeInfo(i);
  auto tensor_info = type_info.GetTensorTypeAndShapeInfo();

  ONNXTensorElementDataType type = tensor_info.GetElementType();
  std::cout << "Input " << i << " : type=" << type << std::endl;

  // print input node dimensions
  input_node_dims = tensor_info.GetShape();
  std::cout << "Input " << i << " : num_dims=" << input_node_dims.size() << std::endl;
  for (std::size_t j = 0; j < input_node_dims.size(); j++) {
    std::cout << "dim " << j << " : " << input_node_dims[j] << std::endl;
  }
}
