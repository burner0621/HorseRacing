import silk1Svg from '../../assets/silks/silk-1.svg'

const RaceTable = () => {
    return (
        <div className="grid grid-flow-row gap-[1px] border rounded-[10px] bg-grey-2 w-full">
            <div className="p-5 grid grid-cols-2 bg-pink-1 rounded-t-[10px]">
                <div className='flex flex-row items-center'>
                    <div className="text-black-2 text-xl leading-6 font-bold">Selections:</div>&nbsp;
                    <div className="text-grey-2 text-xl leading-6 font-medium">Value</div>
                </div>
                <div className="flex flex-row items-center justify-end">
                    <div className="text-black-1 text-base font-medium">1.5% Stake:</div>&nbsp;
                    <div className='text-black-2 text-base font-bold leading-6'>$1,254</div>
                </div>
            </div>
            <div className='grid grid-flow-row gap-[1px]'>
                <div className='selection-table-header'>
                    <div className='race-table-header-item-1'>Silk</div>
                    <div className='race-table-header-item-1'>Num</div>
                    <div className='race-table-header-item-2'>Value</div>
                    <div className='race-table-header-item-2'>BSP</div>
                    <div className='race-table-header-item-2'>Stake</div>
                    <div className='race-table-header-item-2'>Result</div>
                    <div className='race-table-header-item-2 text-right'>Profit</div>
                </div>
                <div className='race-table-body'>{
                    [1,2,3,4].map ((item, idx) =>
                        <div className='selection-table-row' key={idx}>
                            <div className='race-table-col-1'>
                                <img src={silk1Svg} className='w-[26px] h-[21px]' />
                            </div>
                            <div className='race-table-col-1'>1</div>
                            <div className='race-table-col-2'>10</div>
                            <div className='race-table-col-2'>$3.68</div>
                            <div className='race-table-col-2'>$4.68</div>
                            <div className='race-table-col-2'>+24%</div>
                            <div className='race-table-col-2 text-right'>10</div>
                        </div>
                    )}
                    <div className='selection-table-row'>
                        <div className='race-table-col-1 rounded-bl-[10px]'>
                            <img src={silk1Svg} className='w-[26px] h-[21px]' />
                        </div>
                        <div className='race-table-col-1'>1</div>
                        <div className='race-table-col-2'>10</div>
                        <div className='race-table-col-2'>$3.68</div>
                        <div className='race-table-col-2'>$4.68</div>
                        <div className='race-table-col-2'>+24%</div>
                        <div className='race-table-col-2 text-right rounded-br-[10px]'>10</div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default RaceTable