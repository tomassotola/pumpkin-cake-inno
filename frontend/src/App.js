import React from "react";
import Client from "@searchkit/instantsearch-client";
import Searchkit from "searchkit";
import {
  InstantSearch,
  SearchBox,
  Hits,
  RefinementList,
} from "react-instantsearch-hooks-web";
import { Snippet, Highlight } from "react-instantsearch-hooks-web";

// Create a Searchkit client
// This is the configuration for Searchkit, specifying the fields to attributes used for search, facets, etc.
const sk = new Searchkit({
  connection: {
    host: "http://localhost:9200",
    // cloud_id: "my-cloud-id" // if using Elastic Cloud
    // if you're authenticating with username/password
    // https://www.searchkit.co/docs/guides/setup-elasticsearch#connecting-with-usernamepassword
    //auth: {
    //  username: "elastic",
    //  password: "changeme"
    //},
    // if you're authenticating with api key
    // https://www.searchkit.co/docs/guides/setup-elasticsearch#connecting-with-api-key
    // apiKey: "######"
  },
  search_settings: {
    search_attributes: ["Feature", "Summary"],
    result_attributes: [
      "Feature",
      "Summary",
      "Tags",
      "Release",
      "Product",
      "Type",
      "Deprecations",
    ],
    highlight_attributes: ["Feature", "Summary"],
    snippet_attributes: ["Summary", "Release"],
    facet_attributes: [
      { attribute: "Release", field: "Release", type: "string" },
    ],
  },
});

const searchClient = Client(sk);

const HitView = (props) => {
  console.log(props.hit);
  return (
    <div>
      <h2>
        <Highlight attribute="Feature" hit={props.hit} />
      </h2>
      <Snippet attribute="Summary" hit={props.hit} />
      <p>{props.hit.Release}</p>
      <p>{props.hit.Product}</p>
      <p>{props.hit.Type}</p>
      <p>{props.hit.Tags}</p>
      <p>{props.hit.Deprecations}</p>
    </div>
  );
};

const App = () => {
  return (
    <InstantSearch indexName="alteryx_updates" searchClient={searchClient}>
      <SearchBox />
      <div style={{ display: "flex" }}>
        <RefinementList
          attribute="Release"
          style={{ width: "20%", marginTop: "20px", paddingLeft: "20px" }}
        />
        <Hits
          hitComponent={HitView}
          style={{ width: "100%" }}
          title="Releases"
        />
      </div>
    </InstantSearch>
  );
};

export default App;
