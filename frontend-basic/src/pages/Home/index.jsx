import Tracks from '../../components/Tracks'
import Event from '../../components/Event'
import RaceTable from '../../components/RaceTable'
import SelectionTable from '../../components/SelectionTable'
import ScoreChart from '../../components/ScoreChart'

const Home = () => {
    return (
        <div className="grid grid-flow-row gap-5 p-8 sm:p-15 md:p-20 lg:p-28">
            <Tracks />
            <div className='grid grid-cols-4 gap-4'>
                <Event />
                <Event />
                <Event />
                <Event />
            </div>
            <RaceTable />
            <SelectionTable />
            <ScoreChart />
        </div>
    )
}

export default Home