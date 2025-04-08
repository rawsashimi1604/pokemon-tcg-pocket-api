# Pokemon Pocket TCG API

## Notes

### Roadmap

- Achievements
- Profile pictures
- Misc stuff (coins, sleeves, playmats)

### Frontend

- ChatGPT wrapper for MCP
- Meta decks
- Individual Sets (collection)
- Individual Cards

### NFR

- Open API Spec
- TLS Secure
- Rate Limit
- Redocly for spec

### FR

- Image storage (github ref)
- Pokemon card sets
  - name
  - id
  - release date
  - cards (ref to the pokemon card)
  - image link
  - number of cards
- Card
  - [DONE] id
  - [DONE] type (trainer or pokemon)
  - [DONE] name
  - trainer effect (trainer)
  - Stage
  - [DONE] rarity
  - chance to pull (GOOD TO HAVE)
    - Lucky pack
    - Normal Pack
    - Ordering Sequence
  - [DONE] HP (pokemon)
  - ability (pokemon)
  - moves (pokemon)
    - energy cost (qty and type)
    - name
    - damage
    - effect
  - linked cards (evolutions, pokemon)
  - weakness (pokemon)
  - retreat (pokemon)
  - set (link)
  - text
  - artist
    - name
    - URL

### Routes

- GET /api/set
  - Retrieves all card sets
    - Query Params:
      - id
      - sort (add sort options)
- GET /api/set/{setId}
  - Retrieve metadata of card set
- GET /api/card
- GET /api/card/{cardId}

## Quarkus stuff

This project uses Quarkus, the Supersonic Subatomic Java Framework.

If you want to learn more about Quarkus, please visit its website: <https://quarkus.io/>.

## Running the application in dev mode

You can run your application in dev mode that enables live coding using:

```shell script
./mvnw quarkus:dev
```

> **_NOTE:_** Quarkus now ships with a Dev UI, which is available in dev mode only at <http://localhost:8080/q/dev/>.

## Packaging and running the application

The application can be packaged using:

```shell script
./mvnw package
```

It produces the `quarkus-run.jar` file in the `target/quarkus-app/` directory.
Be aware that it’s not an _über-jar_ as the dependencies are copied into the `target/quarkus-app/lib/` directory.

The application is now runnable using `java -jar target/quarkus-app/quarkus-run.jar`.

If you want to build an _über-jar_, execute the following command:

```shell script
./mvnw package -Dquarkus.package.jar.type=uber-jar
```

The application, packaged as an _über-jar_, is now runnable using `java -jar target/*-runner.jar`.

## Creating a native executable

You can create a native executable using:

```shell script
./mvnw package -Dnative
```

Or, if you don't have GraalVM installed, you can run the native executable build in a container using:

```shell script
./mvnw package -Dnative -Dquarkus.native.container-build=true
```

You can then execute your native executable with: `./target/code-with-quarkus-1.0.0-SNAPSHOT-runner`

If you want to learn more about building native executables, please consult <https://quarkus.io/guides/maven-tooling>.

## Provided Code

### REST

Easily start your REST Web Services

[Related guide section...](https://quarkus.io/guides/getting-started-reactive#reactive-jax-rs-resources)
