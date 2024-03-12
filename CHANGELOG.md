# Changelog

## [0.2.4](https://github.com/Broomva/vortex/compare/v0.2.3...v0.2.4) (2024-03-12)


### Bug Fixes

* changed back to local storage ([53a7e50](https://github.com/Broomva/vortex/commit/53a7e500100f1f19d8b7b5c2b3134129b8da3a6b))
* exposed port 4266 ([709f9fa](https://github.com/Broomva/vortex/commit/709f9fa6e530c78c8db2d79deee86caa5a3df2f0))
* removed direct dependencies on dagster for flows resources, reordered examples ([dea04e9](https://github.com/Broomva/vortex/commit/dea04e90a9073e8d47fc9ecba49bda8b26a0d618))
* renaming flows and including base prefect flow ([bda4d72](https://github.com/Broomva/vortex/commit/bda4d72ad1b6e57330d8ab4983dd8f8b7a847416))
* updated dagster to use separate grpc code location server ([661c702](https://github.com/Broomva/vortex/commit/661c702fe4c8130a3e10059128ad7c289f2dcb2e))
* updated dagster_home ([d8e6775](https://github.com/Broomva/vortex/commit/d8e6775ff7ce4c4f5442a3e58a4677bede9f3c16))
* updated dagster.yaml to use cloud storage ([e34e334](https://github.com/Broomva/vortex/commit/e34e334270b994f72fc4b4dbe5954c659960c78a))
* using local code location ([a466993](https://github.com/Broomva/vortex/commit/a466993c339d911e68a8ac19808fe162a2338d92))

## [0.2.3](https://github.com/Broomva/vortex/compare/v0.2.2...v0.2.3) (2024-03-05)


### Bug Fixes

* added fireworks ai as LLM provider ([ff66301](https://github.com/Broomva/vortex/commit/ff66301cc556829d4d0848fba22443b19e053c09))
* fixed typo ([5538f37](https://github.com/Broomva/vortex/commit/5538f37a16b045bddc41c90a3124ed86c76b28f0))
* removed dagster cloud ci/cd files ([7294656](https://github.com/Broomva/vortex/commit/729465643c63630684337fb09ca05994dabd62cf))
* removed unneeded copy commands ([6c54fcb](https://github.com/Broomva/vortex/commit/6c54fcbabd5ea352688578d89b94c6404b9070f0))
* temporary disable of sql tools until more robust guardrails can be implemented ([b05f9e1](https://github.com/Broomva/vortex/commit/b05f9e14be26617415000fa8f80efc60eba03de1))
* testing manually defined gprc server ([c657986](https://github.com/Broomva/vortex/commit/c657986c2306f68ba188bae83a4cc4774627b67a))
* updated requirements ([73d5530](https://github.com/Broomva/vortex/commit/73d55308f6bba9406cf51e5fec9e76b93726ef30))
* updates for dagster docker deploy ([4bc134e](https://github.com/Broomva/vortex/commit/4bc134ef378ff80b602fd75f1caa31ca85f59037))

## [0.2.2](https://github.com/Broomva/vortex/compare/v0.2.1...v0.2.2) (2024-03-04)


### Bug Fixes

* added vercel config file ([821ac7a](https://github.com/Broomva/vortex/commit/821ac7a897e3590641b5880a0389db63e25cb550))
* corrected links ([5ce2c38](https://github.com/Broomva/vortex/commit/5ce2c384ef909aa1b5d2b190ab41f3cb7afe7ed7))
* minor update to prompt ([d13b5b5](https://github.com/Broomva/vortex/commit/d13b5b5603bd9cd825b3ea7ce13411c224427012))
* removed vercel.json file ([f7deb8b](https://github.com/Broomva/vortex/commit/f7deb8b9d7825936a740a788f1ae1b7f4a7cf9a4))
* udpated datamodels ([c713be9](https://github.com/Broomva/vortex/commit/c713be9eefa88c59dccd9b56768a77b799fc0d93))
* updated agent to include sql agent ([b7bcf5f](https://github.com/Broomva/vortex/commit/b7bcf5fbb7f3aea4e49823c7973cf2a6121e3994))
* updated dependencies to correctly use semantic-router. Updated roter defintion to use strategy and factory pattern ([48f2039](https://github.com/Broomva/vortex/commit/48f2039ff523fb2eccf81c8a000ec7ae5038384a))
* updated llm module to be a package, added semantic router module, updated ai agents and prompts modules ([456748a](https://github.com/Broomva/vortex/commit/456748a5d94983f5a7d15d6876d54dec7f03df28))
* updated poetry.lock and pyproject.toml ([acdcfcd](https://github.com/Broomva/vortex/commit/acdcfcdc4054e0c8c1cc4d826eeaf5e76de9e800))
* updated prompt and .env.example template ([f577c51](https://github.com/Broomva/vortex/commit/f577c51b6453fc62382bae3e4e79a6f4036783ab))
* updated prompts ([3bf4167](https://github.com/Broomva/vortex/commit/3bf4167230aebd75c2a5ab4ad8718e0af2270508))
* updated router and routes, added validation for SQL tool via route ([8b37594](https://github.com/Broomva/vortex/commit/8b3759483861d0f2fc9470433fd92c952529bbc1))
* updated routing and session handling for sqlalchemy. Updated logo ([ba28491](https://github.com/Broomva/vortex/commit/ba28491aa702488fa8be3b34a8ef3cfaa6bda821))
* updated to use sqlalchemy env var ([b782c94](https://github.com/Broomva/vortex/commit/b782c94d581316840a62802bc20c3043378478ac))
* updated twilio number ([4fe0f00](https://github.com/Broomva/vortex/commit/4fe0f00db7c8e67294276cf46c0d47f06c3c484e))

## [0.2.1](https://github.com/Broomva/vortex/compare/v0.2.0...v0.2.1) (2024-02-09)


### Bug Fixes

* added user context storage ([8ef6ed0](https://github.com/Broomva/vortex/commit/8ef6ed0316e3e548e776e6fc6b17570243681e96))
* corrected poetry install and fixed pickling of chat history ([bba6d96](https://github.com/Broomva/vortex/commit/bba6d960bd39ade02cc9fbac74b9233c619a64c6))
* corrected twilio module ([2f41de5](https://github.com/Broomva/vortex/commit/2f41de5a4cc518d90bde215f19eebf672ff3af77))
* disabled scrappign tools from default agent ([ebb9530](https://github.com/Broomva/vortex/commit/ebb95303862ce76a12dce371f0d0089c5cd01692))
* fixed deployment scripts in package.json ([7feba6d](https://github.com/Broomva/vortex/commit/7feba6d98f9800b48c00e9af18291e9da16c62c8))
* testint render deploy ([be6592b](https://github.com/Broomva/vortex/commit/be6592bed6f827931c5f554b3c3e30000ea55b74))
* updated poetry to use python 3.9.8 ([a8c736d](https://github.com/Broomva/vortex/commit/a8c736dac11fe2943f3e516ec85e4aa0504bf79e))
* updated twilio wapp modules ([037211f](https://github.com/Broomva/vortex/commit/037211f432423995ef6b42f96360b44d6d87a598))

## [0.2.0](https://github.com/Broomva/vortex/compare/v0.1.6...v0.2.0) (2024-02-08)


### Features

* added vortex agent ([65303bb](https://github.com/Broomva/vortex/commit/65303bbf02e14460cd47757f2d09a13b6a379ec5))


### Bug Fixes

* corrected agents ([18e9253](https://github.com/Broomva/vortex/commit/18e9253f57105a851fdcb84bd6756156772a7665))
* fixed wapp interface with twillio ([9d6d34a](https://github.com/Broomva/vortex/commit/9d6d34a6126516ac429897f75c8ac6cec3460009))
* minor correction to start command ([12569f3](https://github.com/Broomva/vortex/commit/12569f3106565dcd65efd67fd62721918ea8f7a8))
* reordered the folder structure and added some baseline scripts for the wapp interface ([10696b5](https://github.com/Broomva/vortex/commit/10696b5152a7e36212a838ba272395d3d6d28cd5))
* set default twilio number for sandbox env ([2ae30be](https://github.com/Broomva/vortex/commit/2ae30bedafd9d041098b15693ce3eb8761f09912))
* updated examples ([11c5444](https://github.com/Broomva/vortex/commit/11c5444bcaa14cb7a8516d1ffc0b4291d054a6cc))
* updated folder structure ([257908d](https://github.com/Broomva/vortex/commit/257908d1ddc9d7b036843c03b1c93c52c084c341))
* updated llm creation factory ([e207eb5](https://github.com/Broomva/vortex/commit/e207eb57df04a628caa96992f2e578300b4f0033))

## [0.1.6](https://github.com/Broomva/vortex/compare/v0.1.5...v0.1.6) (2024-02-03)


### Bug Fixes

* added baseline FE ([6ae963e](https://github.com/Broomva/vortex/commit/6ae963e1e707aaf90c2cc84873229fe196bd2c87))

## [0.1.5](https://github.com/Broomva/vortex/compare/v0.1.4...v0.1.5) (2024-02-03)


### Bug Fixes

* updated docker and deployment files ([a810bd7](https://github.com/Broomva/vortex/commit/a810bd77762c42ddea030338192586df9c984096))

## [0.1.4](https://github.com/Broomva/vortex/compare/v0.1.3...v0.1.4) (2024-02-02)


### Bug Fixes

* fixing setup to work with dagster deploy ([875093c](https://github.com/Broomva/vortex/commit/875093cb18525a2c06dfacf0dc049897ff0da56c))

## [0.1.3](https://github.com/Broomva/vortex/compare/v0.1.2...v0.1.3) (2024-02-02)


### Bug Fixes

* updated package name ([f6f210e](https://github.com/Broomva/vortex/commit/f6f210e13f214ecae3c4bf743e736803e14e7161))

## [0.1.2](https://github.com/Broomva/vortex-python/compare/v0.1.1...v0.1.2) (2024-02-02)


### Bug Fixes

* updated package name to vortex-python ([d670be1](https://github.com/Broomva/vortex-python/commit/d670be1884b301bf056b23db0a6289133e6c78a6))

## [0.1.1](https://github.com/Broomva/vortex/compare/v0.1.0...v0.1.1) (2024-02-02)


### Bug Fixes

* updated poetry ([343cf15](https://github.com/Broomva/vortex/commit/343cf15c68fd8e77900291463e17550da732b85d))

## 0.1.0 (2024-02-02)


### ⚠ BREAKING CHANGES

* refactored to define vortex baseline structure

### Features

* refactored to define vortex baseline structure ([45b5bc2](https://github.com/Broomva/vortex/commit/45b5bc20192741f2a6c02440c11e5c363987f358))


### Bug Fixes

* formatted with black ([65e68a5](https://github.com/Broomva/vortex/commit/65e68a52f42960c8251a3e3cf983588235c682bc))
