import Datepicker from '../Datepicker';
import auFlag from '../../assets/flags/AU.svg'
import gbFlag from '../../assets/flags/GB.svg'

const Tracks = () => {

    return (
        <div className="w-full grid grid-flow-row gap-[1px] bg-grey-2 rounded-[10px] border border-grey-2">
            <div className="grid grid-cols-2 gap-[1px] w-full">
                <div className="p-8 bg-pink-1 rounded-tl-[10px]">
                    <Datepicker />
                </div>
                <div className="flex flex-row items-center bg-pink-1 text-2xl font-bold justify-end rounded-tr-[10px]">
                    <span className='text-black-2 px-5 py-4'>
                        <div className='text-right text-xl font-bold leading-4'>$128,764</div>
                        <div className='text-right text-[10px] font-normal leading-4'>BANKROLL</div>
                    </span>
                    <span className='text-black-2 px-5 py-4'>
                        <div className='text-right text-xl font-bold leading-4'>$42,184</div>
                        <div className='text-right text-[10px] font-normal leading-4'>TURNOVER</div>
                    </span>
                    <span className='text-black-2 px-5 py-4'>
                        <div className='text-right text-xl font-bold leading-4'>$3,741</div>
                        <div className='text-right text-[10px] font-normal leading-4'>PROFIT</div>
                    </span>
                    <span className='text-black-2 px-5 py-4'>
                        <div className='text-right text-xl font-bold leading-4'>7.43%</div>
                        <div className='text-right text-[10px] font-normal leading-4'>ROI</div>
                    </span>
                </div>
            </div>
            <div className='track-row'>
                <div className='track-header'>Track</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
                <div className='track-header-item'>R1</div>
            </div>
            <div className='track-row'>
                <div className='track-body-header'>
                    <img src={auFlag} className='w-4 h-4 mr-[9px]'/>
                    Flemington
                </div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$532</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$764</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$1053</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-red-600 text-red-2'>-$1231</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$843</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$819</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$3291</span></div>
                <div className='track-body-item text-grey-2'>23m</div>
                <div className='track-body-item text-grey-2'>17:15</div>
                <div className='track-body-item text-grey-2'>17:45</div>
            </div>
            <div className='track-row'>
                <div className='track-body-header'>
                    <img src={gbFlag} className='w-4 h-4 mr-[9px]'/>
                    Ascot
                </div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-red-600 text-red-2'>-$382</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$893</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-red-600 text-red-2'>-$762</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$2842</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$5192</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$1294</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-red-600 text-red-2'>-$543</span></div>
                <div className='track-body-item'><span className='text-shadow-sm shadow-green-600 text-green-1'>$8193</span></div>
                <div className='track-body-item text-grey-2'>8m</div>
                <div className='track-body-item text-grey-2'>17:28</div>
            </div>
        </div>
    )
}

export default Tracks