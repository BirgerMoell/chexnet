import React, { Component } from "react";
import logo from "./logo.svg";
import radiology from "./radiology.png";
import prediction from "./prediction.png";
import "./App.css";
import { css } from "@emotion/core";
import { ClipLoader } from "react-spinners";
import { PDFReader } from "react-read-pdf";

const override = css`
  display: block;
  margin: 0 auto;
  border-color: red;
`;

class App extends Component {
  constructor(props) {
    super(props);
    this.myRef = React.createRef(); // Create a ref object
    this.state = { showPrediction: false, loading: false, pictures: {} };
  }

  handleUpload = async () => {
    console.log("uploaded the image");

    this.setState({
      loading: true
    });
    setTimeout(this.upload, 750);
  };

  upload = async () => {
    this.setState({
      showPrediction: true,
      loading: false
    });

    let file = this.state.selectedFile;
    console.log("the file is", file);

    // if (file) {
    //   try {
    //     const response = await fetch("http://localhost:5000/predict", {
    //       // Your POST endpoint
    //       method: "POST",
    //       headers: { "Content-Type": "application/json" },
    //       body: file
    //       // This is your file object
    //     });
    //     console.log("the response is", response);
    //     const responseJson = response.json();
    //     console.log("the response is", responseJson);
    //   } catch (err) {
    //     console.log(err);
    //   }
    // }
  };

  handleselectedFile = event => {
    this.setState({
      selectedFile: event.target.files[0]
    });
  };

  render() {
    return (
      <div className="App">
        <div className="App-header">
          {/* <img src={radiology} alt="logo" /> */}

          {this.state.selectedFile && (
            <div>
              <img
                className="App-logo"
                src={URL.createObjectURL(this.state.selectedFile)}
              />
            </div>
          )}

          <p>Radiology prediction</p>
          <div>
            <form
              action="http://localhost:5000/uploader"
              method="POST"
              enctype="multipart/form-data"
            >

            <select>
              <option value="Atelectasis">Atelectasis</option>
              <option value="Cardiomegaly">Cardiomegaly</option>
              <option value="Effusion">Effusion</option>
              <option value="Infiltration">Infiltration</option>
              <option value="Mass">Mass</option>
              <option value="Nodule">Nodule</option>
              <option selected value="Pneumonia">Pneumonia</option>
              <option value="Pneumothorax">Pneumothorax</option>
              <option value="Consolidation">Consolidation</option>
              <option value="Edema">Edema</option>
              <option value="Emphysema">Emphysema</option>
              <option value="Fibrosis">Fibrosis</option>
              <option value="Pleural_Thickening">Pleural_Thickening</option>
              <option value="Hernia">Hernia</option>
            </select>
              <input type="file" name="file" onChange={this.handleselectedFile}/>


              <input type="submit" onClick={this.handleUpload} />
            </form>

            {/* <input
              type="file"
              name=""
              id=""
              onChange={this.handleselectedFile}
            />

            <button onClick={this.handleUpload}>Make prediction</button> */}

          </div>

          <div className="Prediction-container">
            <div className="Prediction-loader-container">
              <ClipLoader
                css={override}
                sizeUnit={"px"}
                size={150}
                color={"#123abc"}
                loading={this.state.loading}
              />
            </div>
          </div>

          {this.state.showPrediction && (
            <div className="Prediction-container" id="prediction">
              <h5>Prediction, Pneumonia, 0.06</h5>
              <img className="Prediction-image" src={prediction} />
            </div>
          )}

          <div>
            {" "}
            <a target="_blank" href="https://arxiv.org/pdf/1711.05225.pdf">
              <p>Based on ChexNet</p>
            </a>
            <div style={{ overflow: "scroll", height: 600 }}>
              <PDFReader url="https://arxiv.org/pdf/1711.05225.pdf" />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
