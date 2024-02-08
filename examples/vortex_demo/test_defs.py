from examples.vortex_demo.dags.web_rag_agent import defs


def test_def_can_load():
    assert defs.get_job_def("all_assets_job")
