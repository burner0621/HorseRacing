import successSvg from '../../assets/success.svg'
import uploadSvg from '../../assets/upload.svg'
import silk1Svg from '../../assets/silks/silk-1.svg'

const RaceTable = () => {
    return (
        <div className="grid grid-flow-row bg-grey-2 border rounded-[10px] gap-[1px] w-full">
            <div className="p-5 grid grid-cols-2 bg-pink-1 rounded-t-[10px]">
                <div className="text-black-2 text-xl leading-6 font-bold">Flemington Race 5</div>
                <div className="flex flex-row items-center justify-end gap-2 ">
                    <div className="text-blue-1 text-base font-normal cursor-pointer">flemington-r5.csv</div>
                    <img src={successSvg} className='w-6 h-6' />
                    <div className='cursor-pointer'><img src={uploadSvg} className='w-6 h-6' /></div>
                </div>
            </div>
            <div className='grid grid-flow-row gap-[1px]'>
                <div className='race-table-header'>
                    <div className='race-table-header-item-1'>Silk</div>
                    <div className='race-table-header-item-1'>Num</div>
                    <div className='race-table-header-item-2'>Form Data</div>
                    <div className='race-table-header-item-2'>Framed Odds</div>
                    <div className='race-table-header-item-2'>Betfair Odds</div>
                    <div className='race-table-header-item-2'>Odds Diff%</div>
                    <div className='race-table-header-item-2'>Contender</div>
                    <div className='race-table-header-item-2'>Combined</div>
                </div>
                <div className='race-table-body'>{
                    [1,2,3,4,5,6,7].map ((item, idx) =>
                        <div className='race-table-row' key={idx}>
                            <div className='race-table-col-1'>
                                <img src={silk1Svg} className='w-[26px] h-[21px]' />
                            </div>
                            <div className='race-table-col-1'>1</div>
                            <div className='race-table-col-2'>10</div>
                            <div className='race-table-col-2'>$3.68</div>
                            <div className='race-table-col-2'>$4.68</div>
                            <div className='race-table-col-2'>+24%</div>
                            <div className='race-table-col-2'>10</div>
                            <div className='race-table-col-2'>20</div>
                        </div>
                    )}
                    <div className='race-table-row'>
                        <div className='race-table-col-1 rounded-bl-[10px]'>
                            <img src={silk1Svg} className='w-[26px] h-[21px]' />
                        </div>
                        <div className='race-table-col-1'>1</div>
                        <div className='race-table-col-2'>10</div>
                        <div className='race-table-col-2'>$3.68</div>
                        <div className='race-table-col-2'>$4.68</div>
                        <div className='race-table-col-2'>+24%</div>
                        <div className='race-table-col-2'>10</div>
                        <div className='race-table-col-2 rounded-br-[10px]'>20</div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default RaceTable