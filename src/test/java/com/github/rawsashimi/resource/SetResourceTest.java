package com.github.rawsashimi.resource;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;

import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Test;

@QuarkusTest
class SetResourceTest {
  @Test
  void testHelloEndpoint() {
    given().when().get("/set").then().statusCode(200).body(is("Hello from Quarkus REST"));
  }
}
