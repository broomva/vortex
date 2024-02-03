import Head from 'next/head';

const flows = () => {
    return (
        <div style={{position: 'relative', height: 0, paddingBottom: '56.25%'}}>
            <Head>
                <title>Vortex Flows Embeded</title>
            </Head>
            <iframe
                src="https://broomva.dagster.cloud/prod/"
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    border: 'none'
                }}
            />
        </div>
    );
};

export default flows;
